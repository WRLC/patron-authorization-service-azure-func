from pydantic import BaseModel
from WrapperFunction.models.value_desc import ValueDesc
from WrapperFunction.models.value_only import ValueOnly


# User role parameter object
class Parameter(BaseModel):
    type: ValueOnly = None
    scope: ValueDesc = None
    value: ValueDesc = None
