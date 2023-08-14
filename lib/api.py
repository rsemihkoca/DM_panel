import sys
import requests

sys.path.append('.')
sys.path.append('..')
sys.path.append('../lib')

from lib.config import Config
from lib.headers import Headers
from lib.constants import Constants, Messages


class Api:
    def __init__(self):
        pass

    def CheckUserLoginPassword(self):

        headers = Headers.CheckUserLoginPassword()
        url = f'{Config.base_url}/{Constants.CheckUserLoginPassword}'
        data = {
            'Username': Config.username,
            'Password': Config.password,
            'Language': 'en',
            'Device': None,
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            assert response.status_code == 200
            assert response.json()[Constants.AlertType] == Constants.Success
            assert response.json()[Constants.AlertMessage] == Messages.AlertMessage
            return response.json()
        except requests.exceptions.RequestException as e:
            print('An error occurred:', e)
            return None

    def CheckForLogin(self):

        headers = Headers.CheckForLogin()
        url = f'{Config.base_url}/{Constants.CheckForLogin}'

        params = {
            'username': Config.username,
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            assert response.status_code == 200
            assert response.json()[Constants.AlertType] == Constants.Success
            assert response.json()[Constants.AlertMessage] == Messages.AlertMessage
            return response.json()
        except requests.exceptions.RequestException as e:
            print('An error occurred:', e)
            return None

    def Login(self):
        pass
