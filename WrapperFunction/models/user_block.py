"""
User block object
"""
from datetime import datetime
from pydantic import BaseModel
from WrapperFunction.models.value_desc import ValueDesc


class UserBlock(BaseModel):
    """
    User block object.

    :param block_type: Type of the user block.
    :param block_description: Description of the user block.
    :param block_status: Status of the user block.
    :param block_note: Note for the user block.
    :param created_by: User who created the block.
    :param created_date: Date when the block was created.
    :param expiry_date: Expiry date of the block.
    :param item_loan_id: Item loan ID associated with the block.
    :param block_owner: Owner of the block.
    """
    block_type: ValueDesc | None = None
    block_description: ValueDesc | None = None
    block_status: str | None = None
    block_note: str | None = None
    created_by: str | None = None
    created_date: datetime | None = None
    expiry_date: datetime | None = None
    item_loan_id: str | None = None
    block_owner: str | None = None
