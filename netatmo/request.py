import requests
import netatmo.auth as auth
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    filename='netatmo.log',
    filemode='a',
    format='%(asctime)s -%(levelname)s- %(message)s')


def make_request(url,device_id):
    """
    makes the request to the URL
    :param url:
    :return json object:
    """
    params = {
        'access_token': auth.get_auth_token(),
        'device_id': device_id
    }
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        # returnedContentType = response.headers['Content-Type']
        return response.json()['body']
    except requests.exceptions.HTTPError as error:
        return error.response.status_code+", "+error.response.text
