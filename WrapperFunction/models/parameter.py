"""
Parameter model for user role
"""
from pydantic import BaseModel
from WrapperFunction.models.value_desc import ValueDesc
from WrapperFunction.models.value_only import ValueOnly


class Parameter(BaseModel):
    """
    Parameter model for user role.

    :param type: Type of the parameter.
    :param scope: Scope of the parameter.
    :param value: Value of the parameter.
    """
    type: ValueOnly | None = None
    scope: ValueDesc | None = None
    value: ValueDesc | None = None
