from libs.aws.lambda_utils import lambda_handler

from libs.clients.voice import VoiceAPI, models as v

from typing import Literal

voice_api = VoiceAPI()


@lambda_handler()
def handle(event, context):

    # Retrieve contacts
    contacts_campaignA: list[v.Contact] = voice_api.list_contacts(campaign_id="A")
    contacts_campaignB: list[v.Contact] = voice_api.list_contacts(campaign_id="B")

    # Q1.1 : Build the list of phone numbers that are present in both campaigns
    def list_phone_numbers_in_both_campaigns() -> list[str]: ...

    # Q1.2 : Return the last time each duplicates was called in the two campaigns
    def last_call_date_for_duplicate(
        phone_number: str,
    ) -> dict[Literal["A", "B"], str]: ...

    # --------------------------------------------------------
    duplicates_phone_numbers = list_phone_numbers_in_both_campaigns()
    print(len(duplicates_phone_numbers), "duplicates phone numbers found")

    for duplicate_phone_number in duplicates_phone_numbers:
        last_call_dates = last_call_date_for_duplicate(duplicate_phone_number)
        print(
            duplicate_phone_number,
            f"\tA: {last_call_dates['A'] or 'N/A'}",
            f"\tB: {last_call_dates['B'] or 'N/A'}",
            sep="\n",
        )

    return {}
