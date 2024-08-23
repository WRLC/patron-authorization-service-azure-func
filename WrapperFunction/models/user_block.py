from datetime import datetime
from pydantic import BaseModel
from WrapperFunction.models.value_desc import ValueDesc


# User block object
class UserBlock(BaseModel):
    block_type: ValueDesc = None
    block_description: ValueDesc = None
    block_status: str = None
    block_note: str = None
    created_by: str = None
    created_date: datetime = None
    expiry_date: datetime = None
    item_loan_id: str = None
    block_owner: str = None
