from lib.api import Api


if __name__ == '__main__':
    api = Api()
    response_data = api.CheckUserLoginPassword()
    if response_data:
        print('Response:', response_data)
