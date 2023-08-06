import requests
from ..env import portal_url, service_account_email, service_account_password


class BaseHttpClient:
    api_version: str = None
    token: str = None

    def _create_default_headers(self):
        return {'Authorization': f"Bearer {self.token}"}


class V3ServerClient(BaseHttpClient):
    api_version = 'api/v3'

    def __init__(self):
        self.token = BillingServerClient.login(service_account_email, service_account_password)

    def save_lead(self, message_id: str, email: str) -> str:
        payload = {
            'message_id': message_id,
            'user_email': email
        }
        headers = self._create_default_headers()
        return requests.post(f'{portal_url}/{self.api_version}/user_leads/save', headers=headers, params=payload).json()


class BillingServerClient:
    api_version = 'api'

    @staticmethod
    def login(email: str, password: str) -> str:
        payload = {
            'email': email,
            'password': password
        }
        response = requests.post(f'{portal_url}/{BillingServerClient.api_version}/login', json=payload).json()
        return response['access_token']
