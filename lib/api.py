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
        url = f'{Config.base_url}/{Constants.Account}/{Constants.CheckUserLoginPassword}'
        data = {
            Constants.username: Config.username,
            Constants.password: Config.password,
            Constants.language: 'en',
            Constants.device: None,
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            assert response.status_code == 200
            assert response.json()[Constants.AlertType] == Constants.Success
            assert response.json()[Constants.AlertMessage] == Messages.AlertMessage
            return response
        except requests.exceptions.RequestException as e:
            print('An error occurred:', e)
            return None

    def CheckForLogin(self):

        headers = Headers.CheckForLogin()
        url = f'{Config.base_url}/{Constants.Account}/{Constants.CheckForLogin}'

        params = {
            Constants.username: Config.username
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            assert response.status_code == 200
            assert response.json()[Constants.AlertType] == Constants.Success
            assert response.json()[Constants.AlertMessage] == Messages.AlertMessage
            return response
        except requests.exceptions.RequestException as e:
            print('An error occurred:', e)
            return None

    def Login(self):

        headers = Headers.Login()
        url = f'{Config.base_url}/{Constants.Account}/{Constants.Login}'

        data = {
            Constants.username: Config.username,
            Constants.password: Config.password,
            Constants.language: 'en',
            Constants.device: None,
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            assert response.status_code == 200
            return response
        except requests.exceptions.RequestException as e:
            print('An error occurred:', e)
            return None

    def GetClientTurnoverReportWithActiveBonus(self, authcode, startimelocal, endtimelocal):
        headers = Headers.GetClientTurnoverReportWithActiveBonus(authcode)

        url = f'{Config.base_url}/{Constants.Report}/{Constants.GetClientTurnoverReportWithActiveBonus}'
        data = {
            Constants.StartTimeLocal: startimelocal,
            Constants.EndTimeLocal: endtimelocal,
            Constants.ClientId: None,
            Constants.IsTest: None,
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            assert response.status_code == 200
            return response
        except requests.exceptions.RequestException as e:
            print('An error occurred:', e)
            return None
