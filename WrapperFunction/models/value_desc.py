"""
This module defines a simple value-description object using Pydantic.
"""
from pydantic import BaseModel


# Simple value-description object
class ValueDesc(BaseModel):
    """
    Simple value-description object.

    :param value: The value of the object.
    :param desc: The description of the object.
    """
    value: str | None = None
    desc: str | None = None
