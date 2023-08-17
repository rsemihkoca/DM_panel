import datetime
class Constants:
    Account = 'Account'
    CheckUserLoginPassword = 'CheckUserLoginPassword'
    CheckForLogin = 'CheckForLogin'
    Login = 'Login'

    Report = 'Report'
    GetClientTurnoverReportWithActiveBonus = 'GetClientTurnoverReportWithActiveBonus'

    username = 'username'
    password = 'password'
    language = 'language'
    device = 'device'


    StartTimeLocal = 'StartTimeLocal'
    EndTimeLocal = 'EndTimeLocal'
    ClientId = 'ClientId'
    IsTest = 'IsTest'

    Success = 'success'
    Fail = 'fail'

    AlertType = 'AlertType'
    AlertMessage = 'AlertMessage'

class Tables:
    PlayersExceptToday = 'PlayersExceptToday'
    PlayersToday = 'PlayersToday'

class Messages:
    AlertMessage = 'Operation has completed successfully'

class Dates:
    project_start_date = '02-07-21'
    today = datetime.datetime.today().strftime('%d-%m-%y')
    yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%d-%m-%y')
