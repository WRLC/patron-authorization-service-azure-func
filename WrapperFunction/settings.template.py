doc_message = 'WRLC patron lookup service'  # message to display on /lookup endpoint
endpoint = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/users/'  # Alma User API Get user details endpoint

# These params go on every request
static_params = {'user_id_type': 'all_unique', 'view': 'full', 'expand': 'none'}

api_keys = {
    'inst': 'api_key',  # replace 'inst' with alma IZ code and 'api_key' with User Read API key for IZ
    # Add additional entry for each IZ/key combo
}