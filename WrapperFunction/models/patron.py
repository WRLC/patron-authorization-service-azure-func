from pydantic import BaseModel
from WrapperFunction.models.user_block import UserBlock
from WrapperFunction.models.user_role import UserRole
from WrapperFunction.models.value_desc import ValueDesc


# Patron object (top-level)
class Patron(BaseModel):
    primary_id: str
    full_name: str
    user_group: ValueDesc = None
    user_role: list[UserRole] = None
    status: ValueDesc
    user_block: list[UserBlock] = None
