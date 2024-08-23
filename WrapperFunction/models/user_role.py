from pydantic import BaseModel
from WrapperFunction.models.parameter import Parameter
from WrapperFunction.models.value_desc import ValueDesc


# User role object
class UserRole(BaseModel):
    status: ValueDesc = None
    scope: ValueDesc = None
    role_type: ValueDesc = None
    parameter: list[Parameter] = None
