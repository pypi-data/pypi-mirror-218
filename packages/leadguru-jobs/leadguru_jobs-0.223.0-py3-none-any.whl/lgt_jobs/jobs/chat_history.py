import datetime
from abc import ABC
from typing import Optional, List
from lgt.common.python.lgt_logging import log
from lgt.common.python.slack_client.web_client import SlackWebClient, SlackMessageConvertService
from lgt_data.engine import LeadChat
from lgt_data.enums import DefaultBoards
from lgt_data.model import SlackHistoryMessageModel, UserLeadModel, UserModel, DedicatedBotModel, \
    ExtendedSlackMemberInformation, SlackMemberInformation, LeadModel
from lgt_data.mongo_repository import UserLeadMongoRepository, UserMongoRepository, DedicatedBotRepository, \
    SlackContactUserRepository, LeadMongoRepository, LinkedinContactRepository, BoardsMongoRepository
from pydantic import BaseModel
from ..env import portal_url
from ..runner import BackgroundJobRunner
from ..basejobs import BaseBackgroundJob, BaseBackgroundJobData
from ..smtp import SendMailJobData, SendMailJob
from ..services.web_client import V3ServerClient

"""
Load slack chat history
"""


class LoadChatHistoryJobData(BaseBackgroundJobData, BaseModel):
    user_id: str
    days_ago: Optional[int] = 10
    template_path: str = 'lgt_jobs/templates/new_message_mail_template.html'


class LoadChatHistoryJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return LoadChatHistoryJobData

    def exec(self, data: LoadChatHistoryJobData):
        user = UserMongoRepository().get(data.user_id)
        today = datetime.datetime.utcnow()
        delta = datetime.timedelta(days=data.days_ago)
        dedicated_bots = DedicatedBotRepository().get_user_bots(user.id, only_valid=True)
        for bot in dedicated_bots:
            LoadChatHistoryJob.create_inbox_leads(user, bot)

        leads: List[UserLeadModel] = UserLeadMongoRepository().get_leads(user_id=data.user_id, skip=0, limit=100,
                                                                         from_date=today - delta, archived=False)
        log.info(f"[LoadChatHistoryJob]: processing {len(leads)} for user: {user.email}")

        if not leads:
            return

        last_message = None
        last_message_lead = None
        for lead in leads:
            if not lead.slack_channel:
                continue

            message = LoadChatHistoryJob._update_history(user=user, lead=lead)

            if not message:
                continue

            if not last_message:
                last_message = message
                last_message_lead = lead

            if message.created_at > last_message.created_at and message.user == lead.message.sender_id:
                last_message = message
                last_message_lead = lead

                if lead.last_action_at < last_message.created_at:
                    lead.last_action_at = last_message.created_at
                    UserLeadMongoRepository().update_lead(lead.user_id, lead.id, last_action_at=last_message.created_at)

        has_to_be_notified = not user.new_message_notified_at \
                             or (last_message and last_message.created_at > user.new_message_notified_at)

        if last_message and has_to_be_notified and last_message.user == last_message_lead.message.sender_id:
            LoadChatHistoryJob._notify_about_new_messages(user, last_message_lead, data.template_path)
            UserMongoRepository().set(data.user_id, new_message_notified_at=datetime.datetime.utcnow())

    @staticmethod
    def _merge_chat_histories(saved_chat, current_chat):
        for message in current_chat:
            same_message = [msg for msg in saved_chat if msg.ts == message.ts]
            if same_message:
                same_message[0].text = message.text
                same_message[0].files = message.files
            else:
                saved_chat.append(message)

        return saved_chat

    @staticmethod
    def _update_history(user: UserModel, lead: UserLeadModel) -> Optional[SlackHistoryMessageModel]:
        saved_chat_history = lead.chat_history if lead.chat_history else list()

        bot = DedicatedBotRepository().get_by_user_and_name(user.id, lead.message.name)
        if not bot or bot.invalid_creds:
            return None

        slack_client = SlackWebClient(bot.token, bot.cookies)
        history = slack_client.chat_history(lead.slack_channel)

        if not history['ok']:
            log.error(f'Failed to load chat for the lead: {lead.id}. ERROR: {history.get("error", "")}')
            return None

        messages = [SlackMessageConvertService.from_slack_response(user.email, "slack_files", bot.token, m) for m in
                    history.get('messages', [])]
        messages = sorted(messages, key=lambda x: x.created_at)
        messages = LoadChatHistoryJob._merge_chat_histories(saved_chat=list(saved_chat_history), current_chat=messages)
        chat_history = [message.to_dic() for message in messages]
        UserLeadMongoRepository().update_lead(lead.user_id, lead.id, chat_history=chat_history)
        LeadChat.create_or_update(sender_id=lead.message.sender_id,
                                  user_id=lead.user_id,
                                  workspace=lead.message.name,
                                  chat_history=chat_history)

        return messages[-1] if messages else None

    @staticmethod
    def create_inbox_leads(user: UserModel, dedicated_bot: DedicatedBotModel):
        slack_client = SlackWebClient(dedicated_bot.token, dedicated_bot.cookies)
        conversations_list = slack_client.get_im_list()
        for conversation in conversations_list.get('channels', []):
            sender_id = conversation.get('user')
            im_id = conversation.get('id')
            if sender_id == "USLACKBOT":
                continue
            history = slack_client.chat_history(im_id)
            if not history['ok']:
                log.warning(f'Failed to load chat for the: {dedicated_bot.id}. ERROR: {history.get("error", "")}')
                return

            messages = history.get('messages', [])
            if messages:
                user_lead = UserLeadMongoRepository().get_lead(user.id, sender_id=sender_id)
                if not user_lead:
                    leads_repository = LeadMongoRepository()
                    people = SlackContactUserRepository().find(None, skip=0, limit=1, user=sender_id)[-1]
                    if not people:
                        slack_profile = slack_client.get_profile(sender_id).get('user')
                        people = LoadChatHistoryJob.create_people(slack_profile, dedicated_bot.name)

                    linkedin_contacts = {lc.slack_user: lc for lc in
                                         LinkedinContactRepository().find(slack_user={"$in": [people.user]})}
                    lead = leads_repository.get(str(people.id))
                    if not lead:
                        lead = ExtendedSlackMemberInformation.to_lead(contact=people,
                                                                      linkedin_contacts=linkedin_contacts)
                        leads_repository.add(lead)
                    LoadChatHistoryJob.create_user_lead_if_doesnt_exist(lead, user, im_id)

    @staticmethod
    def _notify_about_new_messages(user: UserModel, lead: UserLeadModel, template_path: str):
        if not lead:
            return

        contact = SlackContactUserRepository().find_one(lead.message.sender_id)
        with open(template_path, mode='r') as template_file:
            html = template_file.read()
            html = html.replace("{sender}", contact.real_name)
            html = html.replace("{view_message_link}", f'{portal_url}/')

            message_data = {
                "html": html,
                "subject": 'New message(s) on LEADGURU',
                "recipient": user.email,
                "sender": None
            }

            SendMailJob().exec(SendMailJobData(**message_data))

    @staticmethod
    def create_people(slack_profile: dict, workspace_name: str):
        member_info: SlackMemberInformation = SlackMemberInformation.from_slack_response(slack_profile, workspace_name)
        SlackContactUserRepository().collection().update_one({"user": member_info.user, "workspace": workspace_name},
                                                             {"$set": member_info.to_dic()}, upsert=True)
        return SlackContactUserRepository().find_one(member_info.user)

    @staticmethod
    def create_user_lead_if_doesnt_exist(lead: LeadModel, user: UserModel, im_id: str):
        user_leads_repository = UserLeadMongoRepository()
        user_lead = user_leads_repository.get_lead(user_id=user.id, lead_id=lead.id)
        if not user_lead:
            inbox_board = BoardsMongoRepository().get(user.id, is_primary=True,
                                                      name=DefaultBoards.Inbox)
            if not inbox_board:
                return
            V3ServerClient().save_lead(lead.message.message_id, user.email)
            UserLeadMongoRepository().update_lead(user.id, str(lead.id),
                                                  slack_channel=im_id,
                                                  board_id=str(inbox_board[0].id),
                                                  last_action_at=datetime.datetime.utcnow())
            log.info(f"[LoadChatHistoryJob]: Added inbox lead {lead.id} for user: {user.email}")
