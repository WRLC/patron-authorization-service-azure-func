# patron-authorization-service-azure-func

FastAPI Azure Functions app for retrieving patron info, including user_role and user_group, from Ex Libris Alma Users API

## Requirements

* Python 3.x
* [Azure Command-Line Interface (CLI)](https://learn.microsoft.com/en-us/cli/azure/)
* [Azure Functions Core Tools ](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)

## Local development

1. Clone the repo: `git clone git@github.com:WRLC/patron-authorization-service-azure-func.git`
2. `cd` into the repo's root directory: `cd patron-authorization-service-azure-func`
3. Create and activate Python virtual environment: `python -m venv .venv` and `source .venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Copy the app .env file: `cp .env.template .env`
6. Edit `.env` to add an Alma API `'key': 'value'` pair for each institution zone (IZ) to the `API_KEYS` environment variable
   * `'key'` = an short code for the IZ; this doesn't need to match anything in Alma, but it will be the value of the 'inst' paremeter in request URLs
   * `'value'` = a working Alma Users API key with read privileges for the IZ (set up in the [Ex Libris Developer Network](https://developers.exlibrisgroup.com/))
7. Run the app: `func start`
8. Access the test endpoint to verify it's working: http://localhost:7071/lookup

## Patron Lookup

The patron lookup URL structure uses two required parameters in the query string:

* `inst` is the key code in `.env` for the IZ API key in the `API_KEYS` environment variable
* `uid` is a unique identifier associated with a patron in Alma for that IZ; this can be the Primary identifier in the Alma user record or an identifier added in the user record's "Identifiers" tab

An API call for a user with a unique identifier `janedoe` at an institution with a key of `mylib` in the `API_KEYS` environmental variable in `WrapperFunction/.env` would be:

```
GET http://localhost:7071/lookup/patron?inst=mylib&uid=janedoe
```

If the API key in `.env` is valid and a user matches the unique identifier, the patron information will be returned in JSON format with the following structure:

```json
{
  "primary_id": "string",
  "full_name": "string",
  "user_group": {
    "value": "string",
    "desc": "string"
  },
  "user_role": [
    {
      "status": {
        "value": "string",
        "desc": "string"
      },
      "scope": {
        "value": "string",
        "desc": "string"
      },
      "role_type": {
        "value": "string",
        "desc": "string"
      },
      "parameter": [
        {
          "type": {
            "value": "string"
          },
          "scope": {
            "value": "string",
            "desc": "string"
          },
          "value": {
            "value": "string",
            "desc": "string"
          }
        }
      ]
    }
  ],
  "status": {
    "value": "string",
    "desc": "string"
  },
  "user_block": [
    {
      "block_type": {
        "value": "string",
        "desc": "string"
      },
      "block_description": {
        "value": "string",
        "desc": "string"
      },
      "block_status": "string",
      "block_note": "string",
      "created_by": "string",
      "created_date": "2024-08-28T12:01:16.224Z",
      "expiry_date": "2024-08-28T12:01:16.224Z",
      "item_loan_id": "string",
      "block_owner": "string"
    }
  ]
}
```

## Standalone node.js app

For a standalone node.js version of this app that uses the same request URL structure and JSON response structure, see [WRLC/patron-authorization-service](https://github.com/WRLC/patron-authorization-service)