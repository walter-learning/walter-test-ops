import os

import requests

from .models import Contact

REMOTE_API_HOST = os.getenv("REMOTE_API_HOST", "")
REMOTE_API_KEY = os.getenv("REMOTE_API_KEY", "")


class VoiceAPI:
    def __init__(self):
        assert REMOTE_API_HOST, "REMOTE_API_HOST is not set"
        assert REMOTE_API_KEY, "REMOTE_API_KEY is not set"

        self.host = REMOTE_API_HOST
        self.session = requests.Session()
        self.session.headers.update({"X-API-KEY": REMOTE_API_KEY})

    def list_contacts(self, campaign_id: str | None = None):
        response = self.session.get(
            f"{self.host}/voice/contacts", params={"campaignId": campaign_id}
        )
        assert (
            response.status_code == 200
        ), f"Failed to get contact : [{response.status_code}] {response.text}"
        return [Contact.model_validate(contact) for contact in response.json()]

    def get_contact(self, contact_id: str):
        response = self.session.get(f"{self.host}/voice/contacts/{contact_id}")
        assert (
            response.status_code == 200
        ), f"Failed to get contact : [{response.status_code}] {response.text}"
        return Contact.model_validate(response.json())

    def update_contact(self, instance: Contact):
        print("⬆️ Updating voice contact")
        print(instance.model_dump_json(indent=4))
