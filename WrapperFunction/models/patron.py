"""
Patron object (top-level)
"""
from pydantic import BaseModel
from WrapperFunction.models.user_block import UserBlock
from WrapperFunction.models.user_role import UserRole
from WrapperFunction.models.value_desc import ValueDesc


class Patron(BaseModel):
    """
    Patron object (top-level).

    :param primary_id: Primary ID of the patron.
    :param full_name: Full name of the patron.
    :param user_group: User group of the patron.
    :param user_role: User role of the patron.
    :param status: Status of the patron.
    :param user_block: User block of the patron.
    """
    primary_id: str
    full_name: str
    user_group: ValueDesc | None = None
    user_role: list[UserRole] | None = None
    status: ValueDesc
    user_block: list[UserBlock] | None = None
