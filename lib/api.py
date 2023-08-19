import sys
import requests

sys.path.append('.')
sys.path.append('..')
sys.path.append('../lib')

from lib.config import Config
from lib.headers import Headers
from lib.constants import Constants, Messages
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Generator

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

    def GetClientTurnoverReportWithActiveBonus(self, authcode, starttimelocal, endtimelocal):
        headers = Headers.GetClientTurnoverReportWithActiveBonus(authcode)

        url = f'{Config.base_url}/{Constants.Report}/{Constants.GetClientTurnoverReportWithActiveBonus}'
        data = {
            Constants.StartTimeLocal: starttimelocal,
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

    def getPlayerReport(self, start_date, end_date):
        self.CheckUserLoginPassword()
        self.CheckForLogin()
        auth_code = self.Login()
        response_data = self.GetClientTurnoverReportWithActiveBonus(auth_code, start_date, end_date)
        if response_data is None:
            return None
        return response_data.json()

    def getPlayerReportDayByDay(self, start_date: str, end_date: str) -> Generator[Optional[Dict[str, Any]], None, None]:
        current_date = datetime.strptime(start_date, '%d-%m-%y')
        end_date_obj = datetime.strptime(end_date, '%d-%m-%y')

        while current_date <= end_date_obj:
            self.CheckUserLoginPassword()
            self.CheckForLogin()
            auth_code = self.Login()
            date = current_date.strftime('%d-%m-%y')

            response_data = self.GetClientTurnoverReportWithActiveBonus(auth_code, date, date)
            if data := response_data if response_data else None:
                yield data.json(), current_date.date()
            else:
                yield None
            current_date += timedelta(days=1)

    def PlayersETL(self, start_date, end_date):
        for i, date in self.getPlayerReportDayByDay(start_date, end_date):
            data = i["Data"]
            if data is None or (isinstance(data, list) and len(data) == 0):
                continue

            formatted_data = [{'Date': date, 'Year': date.year, 'Month': date.month, 'Day': date.day, **entry} for entry in data]
            yield formatted_data