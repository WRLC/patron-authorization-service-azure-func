from pydantic import BaseModel


# Simple value-only object
class ValueOnly(BaseModel):
    value: str = None
