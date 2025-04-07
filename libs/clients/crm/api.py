import os

import requests

from .models import *

REMOTE_API_HOST = os.getenv("REMOTE_API_HOST", "")
REMOTE_API_KEY = os.getenv("REMOTE_API_KEY", "")


class CRMAPI:
    def __init__(self):
        assert REMOTE_API_HOST, "REMOTE_API_HOST is not set"
        assert REMOTE_API_KEY, "REMOTE_API_KEY is not set"

        self.host = REMOTE_API_HOST
        self.session = requests.Session()
        self.session.headers.update({"X-API-KEY": REMOTE_API_KEY})

    def list_contacts(self):
        response = self.session.get(f"{self.host}/crm/contacts")
        assert (
            response.status_code == 200
        ), f"Failed to get contact : [{response.status_code}] {response.text}"
        return [Contact.model_validate(contact) for contact in response.json()]

    def list_agents(self, team: str | None = None):
        response = self.session.get(f"{self.host}/crm/agents", params={"team": team})
        assert (
            response.status_code == 200
        ), f"Failed to get contact : [{response.status_code}] {response.text}"
        return [Agent.model_validate(agent) for agent in response.json()]

    def send_mail(self, email: str, subject: str, body: str):
        print(f"⬆️ Sending email to {email} with subject {subject}")
