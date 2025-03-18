"""
User role object
"""
from pydantic import BaseModel
from WrapperFunction.models.parameter import Parameter
from WrapperFunction.models.value_desc import ValueDesc


class UserRole(BaseModel):
    """
    User role object.

    :param role_type: Type of the user role.
    :param status: Status of the user role.
    :param scope: Scope of the user role.
    :param parameter: Parameters of the user role.
    """
    status: ValueDesc | None = None
    scope: ValueDesc | None = None
    role_type: ValueDesc | None = None
    parameter: list[Parameter] | None = None
