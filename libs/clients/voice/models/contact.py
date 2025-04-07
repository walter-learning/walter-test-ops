from pydantic import BaseModel
from datetime import datetime


class Contact(BaseModel):
    id: str | None = None  # Id of the contact
    campaign_id: str | None = None  # Id of the campaign
    phone: str | None = None  # Phone number of the contact
    retryDate: datetime | None = None  # Force the date of the next call
    lastCallAt: datetime | None = None  # Date of the last call
    assignedAgent: str | None = None  # Id of the agent assigned to the contact
    wrapup: str | None = None  # Wrapup of the contact
    totalCalls: int | None = None  # Total number of calls
    crm_id: str | None = None  # Id of the contact in the CRM
