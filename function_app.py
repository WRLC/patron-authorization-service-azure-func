"""
This is the main function app file. It contains the FastAPI app and the Azure FunctionApp wrapper.
"""
# noinspection PyUnresolvedReferences
from datetime import datetime
import os
import azure.functions as func
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
import requests
from requests import JSONDecodeError

# Load env vars from .env
load_dotenv()
doc_message = os.getenv('DOC_MESSAGE')
endpoint = os.getenv('ENDPOINT')
static_params = eval(os.getenv('STATIC_PARAMS'))
api_keys = eval(os.getenv('API_KEYS'))


class MessageException(Exception):
    """
    Custom exception class for returning error messages
    """
    def __init__(self, code: int, message: str):
        """
        :param code:
        :param message:
        """
        self.code: int = code
        self.message: str = message


class SendException(Exception):
    """
    Custom exception class for returning error messages
    """
    def __init__(self, code: int, body: str):
        """
        :param code:
        :param body:
        """
        self.code: int = code
        self.body: str = body


class ValueOnly(BaseModel):
    """
    Simple value-only object
    """
    value: str = None


class ValueDesc(BaseModel):
    """
    Simple value-description object
    """
    value: str = None
    desc: str = None


class Parameter(BaseModel):
    """
    User role parameter object
    """
    type: ValueOnly = None
    scope: ValueDesc = None
    value: ValueDesc = None


class UserRole(BaseModel):
    """
    User role object
    """
    status: ValueDesc = None
    scope: ValueDesc = None
    role_type: ValueDesc = None
    parameter: list[Parameter] = None


class UserBlock(BaseModel):
    """
    User block object
    """
    block_type: ValueDesc = None
    block_description: ValueDesc = None
    block_status: str = None
    block_note: str = None
    created_by: str = None
    created_date: datetime = None
    expiry_date: datetime = None
    item_loan_id: str = None
    block_owner: str = None


class Patron(BaseModel):
    """
    Patron object (top-level)
    """
    primary_id: str
    full_name: str
    user_group: ValueDesc = None
    user_role: list[UserRole] = None
    status: ValueDesc
    user_block: list[UserBlock] = None


fastapi_app = FastAPI()  # Init FastAPI app


# noinspection PyUnusedLocal
@fastapi_app.exception_handler(MessageException)
async def message_exception_handler(request: Request, exc: MessageException):
    """
    Error handler for MessageException

    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=exc.code,
        content={'message': f'{exc.message}'},
    )


# noinspection PyUnusedLocal
@fastapi_app.exception_handler(SendException)
async def send_exception_handler(reqeust: Request, exc: SendException):
    """
    Error handler for SendException

    :param reqeust:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=exc.code,
        content=exc.body,
    )


@fastapi_app.get("/")
async def root() -> RedirectResponse:
    """
    Home page
    :return:
    """
    return RedirectResponse("/lookup")  # redirect to app


@fastapi_app.get("/lookup")
async def lookup() -> dict:
    """
    Lookup route
    :return:
    """
    return {"message": doc_message}  # return message from settings.py


@fastapi_app.get("/lookup/patron")
async def patron(inst: str = None, uid: str = None) -> Patron:
    """
    Lookup patron

    :param inst:
    :param uid:
    :return:
    """
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


app = func.AsgiFunctionApp(app=fastapi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
