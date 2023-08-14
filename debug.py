from lib.api import Api


if __name__ == '__main__':
    api = Api()
    print("CheckUserLoginPassword")
    response_data = api.CheckUserLoginPassword()
    if response_data:
        print('Response:', response_data)

    print("CheckForLogin")
    response_data = api.CheckForLogin()

    if response_data:
        print('Response:', response_data)

