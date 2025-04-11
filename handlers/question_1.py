from libs.aws.lambda_utils import lambda_handler

from libs.clients.voice import VoiceAPI, models as v

from typing import Literal

voice_api = VoiceAPI()


@lambda_handler()
def handle(event, context):

    # Retrieve contacts from the API
    contacts_campaignA: list[v.Contact] = voice_api.list_contacts(campaign_id="A")
    contacts_campaignB: list[v.Contact] = voice_api.list_contacts(campaign_id="B")

    # --------------------------------------------------------

    def list_phone_numbers_in_both_campaigns() -> list[str]:
        print("👉", len(contacts_campaignA), "contacts in campaign A")
        print("👉", len(contacts_campaignB), "contacts in campaign B")
        example_contact = contacts_campaignA[0]
        print("📞", example_contact.phone)
        # Q1.1 : Implement the logic to return the list of phone numbers that are present in both campaigns
        # ... <<<<<<<<<<<<
        return []

    def last_call_date_for_duplicate(
        phone_number: str,
    ) -> dict:
        output = {"A": None, "B": None}
        # Q1.2 : Implement the logic to return the last time a phone number was called in the two campaigns
        # ... <<<<<<<<<<<<
        return output

    # --------------------------------------------------------

    duplicates_phone_numbers = list_phone_numbers_in_both_campaigns()

    if event["action"] == "list_phone_numbers_in_both_campaigns":
        print(len(duplicates_phone_numbers), "duplicates phone numbers found")

    if event["action"] == "last_call_date_for_duplicate":
        for duplicate_phone_number in duplicates_phone_numbers:
            last_call_dates = last_call_date_for_duplicate(duplicate_phone_number)
            print(
                duplicate_phone_number,
                f"\tA: {last_call_dates['A'] or 'N/A'}",
                f"\tB: {last_call_dates['B'] or 'N/A'}",
                sep="\n",
            )

    return {}
