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

    print(f"🔵 Retrieve contact `{event.contactId}` from the API")
    voice_contact = (
        voice_api.get_contact(contact_id=event.contactId) if event.contactId else None
    )
    if voice_contact:
        # ------------------------------------------------------------
        # STEP 1 : If callBackDate was set to tomorrow or after update the retryDate
        if (event.wrapup or "").lower() == "rappel":
            print(f"🔵 The callback date is set to `{event.callBackDate}`")
            if (
                event.callBackDate
                and event.callBackDate <= datetime.today() + timedelta(days=1)
            ):
                print(f"🔵 Update retryDate to `{event.callBackDate}`")
                voice_contact.retryDate = event.callBackDate
                voice_api.update_contact(instance=voice_contact)

        # ------------------------------------------------------------
        # STEP 2 : If Support in wrapUp, assign the support agent with the least number of contacts in campaign B
        elif "support" in (event.wrapup or "").lower():
            assigned_agent_username = None
            agents_support: list[crm.Agent] = crm_api.list_agents(team="support")
            contacts_campaignB: list[v.Contact] = voice_api.list_contacts(
                campaign_id="B"
            )
            # Q2.1 : Assign the contact to the support agent with the least number of contacts in campaign B
            # ... <<<<<<<<<<<<
            print("🔵 Assign to agent", assigned_agent_username)
            voice_contact.assignedAgent = assigned_agent_username
            voice_api.update_contact(instance=voice_contact)

    return {}
