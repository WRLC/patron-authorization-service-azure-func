import azure.functions as func
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
import requests
from requests import JSONDecodeError
from datetime import datetime
from WrapperFunction.settings import api_keys, endpoint, static_params, doc_message


# Create custom exception class
class MessageException(Exception):
    def __init__(self, code: int, message: str):
        self.code: int = code
        self.message: str = message


# SendException class
class SendException(Exception):
    def __init__(self, code: int, body: str):
        self.code: int = code
        self.body: str = body


fastapi_app = FastAPI()  # Init FastAPI app


# Simple value-only object
class ValueOnly(BaseModel):
    value: str = None


# Simple value-description object
class ValueDesc(BaseModel):
    value: str = None
    desc: str = None


# User role parameter object
class Parameter(BaseModel):
    type: ValueOnly = None
    scope: ValueDesc = None
    value: ValueDesc = None


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


# User role object
class UserRole(BaseModel):
    status: ValueDesc = None
    scope: ValueDesc = None
    role_type: ValueDesc = None
    parameter: list[Parameter] = None


# Patron object (top-level)
class Patron(BaseModel):
    primary_id: str
    full_name: str
    user_group: ValueDesc = None
    user_role: list[UserRole] = None
    status: ValueDesc
    user_block: list[UserBlock] = None


# Error handler for MessageException
# noinspection PyUnusedLocal
@fastapi_app.exception_handler(MessageException)
async def message_exception_handler(request: Request, exc: MessageException):
    return JSONResponse(
        status_code=exc.code,
        content={'message': f'{exc.message}'},
    )


# Error handler for SendException
# noinspection PyUnusedLocal
@fastapi_app.exception_handler(SendException)
async def send_exception_handler(reqeust: Request, exc: SendException):
    return JSONResponse(
        status_code=exc.code,
        content=exc.body,
    )


# Home page
@fastapi_app.get("/")
async def root():
    return RedirectResponse("/lookup")  # redirect to app


# Lookup route
@fastapi_app.get("/lookup")
async def lookup():
    return {"message": doc_message}  # return message from settings.py


# Lookup patron
@fastapi_app.get("/lookup/patron")
async def patron(inst: str = None, uid: str = None) -> Patron:
    if uid is None:  # If uid param not in key, return 400
        raise MessageException(400, 'No uid in request. Include it in your query string: ?uid=xxxxxx')

    if inst is None:  # If inst param not in key, return 400
        raise MessageException(400, 'No institution in request. Include it in your query string: ?inst=xxxxxx')

    if inst not in api_keys:  # If inst not found in API keys, return 400
        raise MessageException(400, 'Unknown institution')

    payload = static_params  # get static params from settings
    payload.update({'apikey': api_keys[inst], 'format': 'json'})  # append inst's API key

    try:
        r = requests.get(endpoint + uid, params=payload)  # make Alma User API call
        r.raise_for_status()  # raise HTTP errors as exceptions

    except requests.exceptions.RequestException as err:  # If request raised an exception...
        raise SendException(500, err.response.text)  # ...return a 500 error

    try:
        attributes = r.json()  # get the user attributes
    except JSONDecodeError as errj:  # If the response isn't valid json...
        raise SendException(404, errj.response.text)  # ...return a 404 error

    return Patron(
        primary_id=attributes['primary_id'],
        full_name=attributes['full_name'],
        user_group=attributes['user_group'],
        user_role=attributes['user_role'],
        status=attributes['status'],
        user_block=attributes['user_block']
    )