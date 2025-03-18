"""
This is the main entry point for the Azure Function.
"""
# pylint: disable=C0103
# noinspection PyUnresolvedReferences
import os
from ast import literal_eval
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
import requests  # type:ignore[import-untyped]
from requests import JSONDecodeError
from dotenv import load_dotenv
from WrapperFunction.models.patron import Patron  # pylint: disable=import-error
from WrapperFunction.models.exceptions import MessageException, SendException  # pylint: disable=import-error

# Load env vars from .env
load_dotenv()
doc_message = os.getenv('DOC_MESSAGE')
endpoint = os.getenv('ENDPOINT') or ''
static_params = literal_eval(os.getenv('STATIC_PARAMS') or '{}')  # Static params for Alma API
api_keys = literal_eval(os.getenv('API_KEYS') or '{}')  # API keys for Alma API

fastapi_app = FastAPI()  # Init FastAPI app


# noinspection PyUnusedLocal
@fastapi_app.exception_handler(MessageException)
async def message_exception_handler(request: Request, exc: MessageException):  # pylint: disable=unused-argument
    """
    Custom error handler for MessageException.

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
async def send_exception_handler(reqeust: Request, exc: SendException):  # pylint: disable=unused-argument
    """
    Custom error handler for SendException.

    :param reqeust:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=exc.code,
        content=exc.body,
    )


# Home page
@fastapi_app.get("/")
async def root() -> RedirectResponse:
    """
    Redirect to lookup page.

    :return: RedirectResponse
    """
    return RedirectResponse("/lookup")  # redirect to app


# Lookup route
@fastapi_app.get("/lookup")
async def lookup() -> dict:
    """
    Lookup page.

    :return:
    """
    return {"message": doc_message}  # return message from settings.py


# Lookup patron
@fastapi_app.get("/lookup/patron")
async def patron(inst: str | None = None, uid: str | None = None) -> Patron:
    """
    Lookup patron by UID.

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
        r = requests.get(endpoint + uid, params=payload, timeout=60)  # make Alma User API call
        r.raise_for_status()  # raise HTTP errors as exceptions

    except requests.exceptions.RequestException as err:  # If request raised an exception...
        raise MessageException(400, f'Error: {err}') from err  # ...return a 400 error

    try:
        attributes = r.json()  # get the user attributes
    except JSONDecodeError as errj:  # If the response isn't valid json...
        raise SendException(404, errj.response.text) from errj  # ...return a 404 error

    return Patron(
        primary_id=attributes['primary_id'],
        full_name=attributes['full_name'],
        user_group=attributes['user_group'],
        user_role=attributes['user_role'],
        status=attributes['status'],
        user_block=attributes['user_block']
    )
