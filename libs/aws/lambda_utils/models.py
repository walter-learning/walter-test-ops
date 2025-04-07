from pydantic import BaseModel, Extra

class BaseEvent(BaseModel, extra=Extra.ignore):
    ...