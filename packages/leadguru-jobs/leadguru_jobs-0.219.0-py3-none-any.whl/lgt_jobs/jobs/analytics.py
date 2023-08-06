import datetime
from abc import ABC
from typing import Optional, List

from pydantic import BaseModel
from pymongo import MongoClient

from ..basejobs import BaseBackgroundJob, BaseBackgroundJobData
from ..env import mongo_connection_string

"""
Track analytics
"""


class TrackAnalyticsJobData(BaseBackgroundJobData, BaseModel):
    data: str
    name: str
    event: str
    extra_ids: List[str] = []
    attributes: Optional[List]
    created_at: datetime.datetime


class TrackAnalyticsJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return TrackAnalyticsJobData

    def exec(self, data: TrackAnalyticsJobData):
        with MongoClient(mongo_connection_string) as client:
            db = client.lgt_analytics
            event_type = data.event
            if event_type == 'message-received':
                collection_name = 'received_messages'
            elif type == 'message-filtered-in':
                collection_name = 'filtered_messages'
            else:
                collection_name = event_type

            analytics_id = db[collection_name].insert_one(data.dict()).inserted_id
            print(f'entry with id {analytics_id} has been recorded into {collection_name}')
