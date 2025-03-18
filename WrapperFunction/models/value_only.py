"""
ValueOnly model
"""
from pydantic import BaseModel


# Simple value-only object
class ValueOnly(BaseModel):
    """
    Simple value-only object.
    """
    value: str | None = None
