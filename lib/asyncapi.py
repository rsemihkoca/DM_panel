import sys
import requests
import httpx
import asyncio
sys.path.append('.')
sys.path.append('..')
sys.path.append('../lib')

from lib.config import Config
from lib.headers import Headers
from lib.constants import Constants, Messages
from typing import Optional, Dict, Any, AsyncGenerator
from datetime import datetime, timedelta

class AsyncAPI:

    def __init__(self):
        pass
    async def CheckUserLoginPassword(self):

        headers = Headers.CheckUserLoginPassword()
        url = f'{Config.base_url}/{Constants.Account}/{Constants.CheckUserLoginPassword}'
        data = {
            Constants.username: Config.username,
            Constants.password: Config.password,
            Constants.language: 'en',
            Constants.device: None,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()
                assert response.status_code == 200
                assert response.json()[Constants.AlertType] == Constants.Success
                assert response.json()[Constants.AlertMessage] == Messages.AlertMessage
                return response
            except httpx.RequestError as e:
                print('An error occurred:', e)
                return None

    async def CheckForLogin(self):

        headers = Headers.CheckForLogin()
        url = f'{Config.base_url}/{Constants.Account}/{Constants.CheckForLogin}'
        params = {
            Constants.username: Config.username
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                assert response.status_code == 200
                assert response.json()[Constants.AlertType] == Constants.Success
                assert response.json()[Constants.AlertMessage] == Messages.AlertMessage
                return response
            except httpx.RequestError as e:
                print('An error occurred:', e)
                return None

    async def Login(self):

        headers = Headers.Login()
        url = f'{Config.base_url}/{Constants.Account}/{Constants.Login}'
        data = {
            Constants.username: Config.username,
            Constants.password: Config.password,
            Constants.language: 'en',
            Constants.device: None,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()
                assert response.status_code == 200
                return response
            except httpx.RequestError as e:
                print('An error occurred:', e)
                return None

    async def GetClientTurnoverReportWithActiveBonus(self, authcode, starttimelocal, endtimelocal):
        headers = Headers.GetClientTurnoverReportWithActiveBonus(authcode)
        url = f'{Config.base_url}/{Constants.Report}/{Constants.GetClientTurnoverReportWithActiveBonus}'
        data = {
            Constants.StartTimeLocal: starttimelocal,
            Constants.EndTimeLocal: endtimelocal,
            Constants.ClientId: None,
            Constants.IsTest: None,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()
                assert response.status_code == 200
                return response
            except httpx.RequestError as e:
                print('An error occurred:', e)
                return None

    async def getPlayerReportDayByDay(self, start_date: str, end_date: str) -> AsyncGenerator[Optional[Dict[str, Any]], None]:
        current_date = datetime.strptime(start_date, '%d-%m-%Y')
        end_date_obj = datetime.strptime(end_date, '%d-%m-%Y')

        while current_date <= end_date_obj:
            await self.CheckUserLoginPassword()
            await self.CheckForLogin()
            response_data = await self.Login()
            auth_code = response_data.headers['authentication']

            date = current_date.strftime('%d-%m-%y')
            response_data = await self.GetClientTurnoverReportWithActiveBonus(auth_code, date, date)
            if data := response_data.json() if response_data else None:
                yield data, current_date.date()
            else:
                yield None

            current_date += timedelta(days=1)


    async def PlayersETL(self, start_date, end_date):
        async for i, date in self.getPlayerReportDayByDay(start_date, end_date):
            data = i["Data"]
            if data is None or (isinstance(data, list) and len(data) == 0):
                continue

            formatted_data = [{'Date': date, 'Year': date.year, 'Month': date.month, 'Day': date.day, **entry} for entry in data]
            yield formatted_data
