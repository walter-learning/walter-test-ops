from pydantic import BaseModel
from datetime import datetime


class Contact(BaseModel):
    id: str | None = None
    first_name: str | None = None
    last_name: str
    email: str | None = None
    phone: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
