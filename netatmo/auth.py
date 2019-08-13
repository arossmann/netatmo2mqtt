import requests
import configparser

def authenticate():
    """
    get the authentication token
    :return: auth token
    """
    # read config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    # set variables

    header = {}

    payload = {'grant_type': 'password',
           'username': config['NETATMO']['USERNAME'],
           'password': config['NETATMO']['PASSWORD'],
           'client_id':config['NETATMO']['CLIENT_ID'],
           'client_secret': config['NETATMO']['SECRET'],
           'scope': config['NETATMO']['SCOPE']}
    try:
        response = requests.post(config['NETATMO']['TOKEN_URL'], data=payload)
        response.raise_for_status()
        header["access_token"] = response.json()["access_token"]
        # access_token=response.json()["access_token"]
        header["refresh_token"] = response.json()["refresh_token"]
        header["scope"] = response.json()["scope"]
    except requests.exceptions.HTTPError as error:
        print(error.response.status_code, error.response.text)
    return header

def get_auth_token():
    """
    getting the header with authorization token
    :return: the access token
    """
    header = authenticate()
    return header["access_token"]
