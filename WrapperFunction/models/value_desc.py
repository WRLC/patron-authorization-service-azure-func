from pydantic import BaseModel


# Simple value-description object
class ValueDesc(BaseModel):
    value: str = None
    desc: str = None
