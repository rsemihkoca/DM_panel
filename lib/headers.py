from lib.config import Config
from fake_useragent import UserAgent
from urllib.parse import urlparse
parsed_url = urlparse(Config.base_url)
subdomain, _, domain = parsed_url.netloc.partition('.')

class Headers:

    @staticmethod
    def CheckUserLoginPassword():
        ua = UserAgent()
        user_agent = ua.random

        return {
            'authority': domain,
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'tr',
            'access-control-allow-credentials': 'true',
            'content-type': 'application/json;charset=UTF-8',
            'origin': subdomain,
            'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': user_agent,
            'x-requested-with': 'XMLHttpRequest',
        }

    @staticmethod
    def CheckForLogin():
        ua = UserAgent()
        user_agent = ua.random

        return {
            'authority': domain,
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'tr',
            'access-control-allow-credentials': 'true',
            'authentication': '',
            # 'cookie': '',
            'dnt': '1',  # Do Not Track
            'origin': subdomain,
            'referer': subdomain + '/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': user_agent,
            'x-requested-with': 'XMLHttpRequest',
        }

    @staticmethod
    def Login():
        ua = UserAgent()
        user_agent = ua.random

        return {
            'authority': domain,
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'tr',
            'access-control-allow-credentials': 'true',
            'authentication': '',
            'content-type': 'application/json;charset=UTF-8',
            # 'cookie': '',
            'dnt': '1',  # Do Not Track
            'origin': subdomain,
            'referer': subdomain + '/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': user_agent,
            'x-requested-with': 'XMLHttpRequest',
        }

    @staticmethod
    def GetClientTurnoverReportWithActiveBonus(authcode: str):
        ua = UserAgent()
        user_agent = ua.random

        return {
            'authority': domain,
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'tr',
            'access-control-allow-credentials': 'true',
            'authentication': authcode,
            'content-type': 'application/json;charset=UTF-8',
            # 'cookie': '',
            'dnt': '1',  # Do Not Track
            'origin': subdomain,
            'referer': subdomain + '/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': user_agent,
            'x-requested-with': 'XMLHttpRequest',
        }