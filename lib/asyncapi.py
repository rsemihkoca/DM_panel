import sys
import requests
from functools import wraps
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



    def retry_on_readtimeout(retries=3):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                for i in range(retries):
                    try:
                        return await func(*args, **kwargs)
                    except httpx.ReadTimeout:
                        if i < retries - 1:  # i starts from 0
                            print(f"ReadTimeout encountered. Retrying... {i + 1}/{retries}")
                            continue
                        else:
                            print("Max retries reached. Aborting.")
                            raise
                    except Exception as e:  # Handle other exceptions
                        print('An error occurred:', e)
                        return None

            return wrapper

        return decorator

    @retry_on_readtimeout()
    async def send_request(self, method, url, headers, data=None, params=None):
        async with httpx.AsyncClient(timeout=5) as client:
            if method == "POST":
                response = await client.post(url, headers=headers, json=data, params=params)
            elif method == "GET":
                response = await client.get(url, headers=headers, params=params)
            # Add more methods as needed, e.g., PUT, DELETE, etc.
            else:
                raise ValueError(f"Unsupported method: {method}")
            return response



    async def CheckUserLoginPassword(self):

        headers = Headers.CheckUserLoginPassword()
        url = f'{Config.base_url}/{Constants.Account}/{Constants.CheckUserLoginPassword}'
        data = {
            Constants.username: Config.username,
            Constants.password: Config.password,
            Constants.language: 'en',
            Constants.device: None,
        }
        # post request
        return await self.send_request("POST", url, headers, data)

    async def CheckForLogin(self):

        headers = Headers.CheckForLogin()
        url = f'{Config.base_url}/{Constants.Account}/{Constants.CheckForLogin}'
        params = {
            Constants.username: Config.username
        }
        # get request
        return await self.send_request("GET", url, headers, params)

    async def Login(self):

        headers = Headers.Login()
        url = f'{Config.base_url}/{Constants.Account}/{Constants.Login}'
        data = {
            Constants.username: Config.username,
            Constants.password: Config.password,
            Constants.language: 'en',
            Constants.device: None,
        }
        # post request
        return await self.send_request("POST", url, headers, data)

    async def GetClientTurnoverReportWithActiveBonus(self, authcode, starttimelocal, endtimelocal):
        headers = Headers.GetClientTurnoverReportWithActiveBonus(authcode)
        url = f'{Config.base_url}/{Constants.Report}/{Constants.GetClientTurnoverReportWithActiveBonus}'
        data = {
            Constants.StartTimeLocal: starttimelocal,
            Constants.EndTimeLocal: endtimelocal,
            Constants.ClientId: None,
            Constants.IsTest: None,
        }
        # post request
        return await self.send_request("POST", url, headers, data)

    async def getPlayerReportDayByDay(self, start_date: str, end_date: str, cron: bool) -> AsyncGenerator[Optional[Dict[str, Any]], None]:
        current_date = datetime.strptime(start_date, '%d-%m-%y')
        end_date_obj = datetime.strptime(end_date, '%d-%m-%y')

        while current_date <= end_date_obj:
            await self.CheckUserLoginPassword()
            await self.CheckForLogin()
            response_data = await self.Login()
            if response_data is None:
                raise Exception('Login failed')


            auth_code = response_data.headers['authentication']

            date = current_date.strftime('%d-%m-%y')
            response_data = await self.GetClientTurnoverReportWithActiveBonus(auth_code, date, date)

            if response_data is None:
                raise Exception('GetClientTurnoverReportWithActiveBonus failed')

            if data := response_data.json() if response_data else None:
                yield data, current_date.date()
            else:
                yield None

            if not cron:
                current_date += timedelta(days=1)


    async def PlayersETL(self, start_date, end_date, cron):
        async for i, date in self.getPlayerReportDayByDay(start_date, end_date, cron):
            data = i["Data"]
            if data is None or (isinstance(data, list) and len(data) == 0):
                continue

            formatted_data = [{'Date': date, 'Year': date.year, 'Month': date.month, 'Day': date.day, **entry} for entry in data]
            yield formatted_data
    async def run_cron(self, generator, interval_seconds: int):
        while True:
            print(f"Starting the cron job... {datetime.now()}")
            async for data in generator:
                print(f"Job done! Waiting for {interval_seconds} seconds...")
                await asyncio.sleep(interval_seconds)
                yield data
