from libs.aws.lambda_utils import lambda_handler, BaseEvent

from datetime import datetime, timedelta

from libs.clients.voice import VoiceAPI, models as v
from libs.clients.crm import CRMAPI, models as crm

voice_api = VoiceAPI()
crm_api = CRMAPI()


class Event(BaseEvent):
    agent: str | None = None
    callDurationInSeconds: str | None = None
    callBackDate: str | None = None
    callEnd: str | None = None
    callId: str | None = None
    callResult: str | None = None
    callStart: str | None = None
    callType: str | None = None
    campaignId: str | None = None
    campaignName: str | None = None
    contactId: str | None = None
    contactPhone: str | None = None
    conversationDuration: str | None = None
    displayedPhoneNumber: str | None = None
    wrapupComment: str | None = None
    wrapup: str | None = None


@lambda_handler(model=Event)
def handle(event: Event, context):

    print(f"🔵 Retrieve contact `{event.contactId}`")
    voice_contact = (
        voice_api.get_contact(contact_id=event.contactId) if event.contactId else None
    )
    if voice_contact:
        print(f"🔵 Contact information :")
        print(voice_contact.model_dump_json(indent=4))

        # ------------------------------------------------------------
        # STEP 1 : If callBackDate was set to tomorrow or after update the retryDate
        if (event.wrapup or "").lower() == "rappel":
            if (
                event.callBackDate
                and event.callBackDate <= datetime.today() + timedelta(1)
            ):
                voice_contact.retryDate = event.callBackDate  # type: ignore
                voice_api.update_contact(instance=voice_contact)

        # ------------------------------------------------------------
        # STEP 2 : If Support in wrapUp, assign the support agent with the least number of contacts in campaign B
        elif "support" in (event.wrapup or "").lower():
            ...

    return {}
