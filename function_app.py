"""
Azure Function App for FastAPI
"""
# pylint: disable=C0103
# noinspection PyUnresolvedReferences
import os
from typing import Any
from ast import literal_eval
import azure.functions as func
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import requests  # type:ignore[import-untyped]
from requests import JSONDecodeError
from dotenv import load_dotenv

# Load env vars from .env
load_dotenv()
doc_message = os.getenv('DOC_MESSAGE')
endpoint = os.getenv('ENDPOINT') or ''
static_params = literal_eval(os.getenv('STATIC_PARAMS') or '{}')  # Static params for Alma API
api_keys = literal_eval(os.getenv('API_KEYS') or '{}')  # API keys for Alma API

fastapi_app = FastAPI()  # Init FastAPI app


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
async def patron(inst: str | None = None, uid: str | None = None) -> dict[str, Any]:
    """
    Lookup patron by UID.

    :param inst:
    :param uid:
    :return:
    """
    if uid is None:  # If uid param not in key, return 400
        raise HTTPException(400, 'No uid in request. Include it in your query string: ?uid=xxxxxx')

    if inst is None:  # If inst param not in key, return 400
        raise HTTPException(400, 'No institution in request. Include it in your query string: ?inst=xxxxxx')

    if inst not in api_keys:  # If inst not found in API keys, return 400
        raise HTTPException(400, 'Unknown institution')

    payload = static_params  # get static params from settings
    payload.update({'apikey': api_keys[inst], 'format': 'json'})  # append inst's API key

    try:
        r = requests.get(endpoint + uid, params=payload, timeout=60)  # make Alma User API call
        r.raise_for_status()  # raise HTTP errors as exceptions

    except requests.exceptions.RequestException as err:  # If request raised an exception...
        raise HTTPException(status_code=404, detail='User not found in Alma') from err  # ...return a 404

    try:
        attributes = r.json()  # get the user attributes
    except JSONDecodeError as errj:  # If the response isn't valid json...
        raise HTTPException(status_code=503, detail='Unable to parse Alma user record') from errj  # ...return a 503

    return {
        'primary_id': attributes['primary_id'],
        'full_name': attributes['full_name'],
        'user_group': attributes['user_group'],
        'user_role': attributes['user_role'],
        'status': attributes['status'],
        'user_block': attributes['user_block']
    }

app = func.AsgiFunctionApp(app=fastapi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
