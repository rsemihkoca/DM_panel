import datetime
from database import models


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

    Authentication = 'Authentication'


class Tables:
    Players = 'Players'


class TableFields:
    Players = models.Players.get_column_names()
    GeneralSituationDashboard = models.GeneralSituationDashboard.get_column_names()
    AffiliateDashboard = models.AffiliateDashboard.get_column_names()
    NaturalMembersDashboard = models.NaturalMembersDashboard.get_column_names()


class Messages:
    AlertMessage = 'Operation has completed successfully'


class Dates:
    project_start_date: str = '02-07-21'
    today: str = datetime.datetime.today().strftime('%d-%m-%y')
    yesterday: str = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%d-%m-%y')

class CommissionCoefficients:

    def __init__(self, SFK: float, CFK: float, FOK: float):
        self.__SFK = SFK
        self.__CFK = CFK
        self.__FOK = FOK

    @property
    def SFK(self):
        return self.__SFK

    @SFK.setter
    def SFK(self, value):
        # check value is between 0 and 1
        if value < 0 or value > 1:
            raise ValueError('SFK must be between 0 and 1')
        else:
            self.__SFK = value

    @property
    def CFK(self):
        return self.__CFK

    @CFK.setter
    def CFK(self, value):
        # check value is between 0 and 1
        if value < 0 or value > 1:
            raise ValueError('CFK must be between 0 and 1')
        else:
            self.__CFK = value

    @property
    def FOK(self):
        return self.__FOK

    @FOK.setter
    def FOK(self, value):
        # check value is between 0 and 1
        if value < 0 or value > 1:
            raise ValueError('FOK must be between 0 and 1')
        else:
            self.__FOK = value

