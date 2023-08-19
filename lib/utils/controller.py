import logging
import polars as pl
from datetime import datetime, timedelta
from lib.api import Api
from lib.constants import Constants, Messages, Dates, Tables, TableFields
from lib.utils.helper import profiler, create_date_list, write_to_csv
from lib.utils import validators
from database.crud import Crud
from database.models import PlayersExceptToday, PlayersToday
from logging.handlers import RotatingFileHandler
from typing import Generator, Optional, Any, Dict


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Console Handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

# File Handler with rotation
fh = RotatingFileHandler('app.log', maxBytes=5*1024*1024, backupCount=5) # 5MB per file, with backup up to 5 files.
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

class Controller:

    def __init__(self):
        self.api = Api()
        self.logger = logger
        self.crud = Crud()
    def __CheckUserLoginPassword__(self):
        # self.logger.info("CheckUserLoginPassword")
        response_data = self.api.CheckUserLoginPassword()
        # self.logger.info("OK")

    def __CheckForLogin__(self):
        # self.logger.info("CheckForLogin:")
        response_data = self.api.CheckForLogin()
        # self.logger.info("OK")
    def __Login__(self):
        # self.logger.info("Login:")
        response_data = self.api.Login()
        authcode = response_data.headers['authentication']
        self.logger.info("authcode: " + authcode)
        # self.logger.info("OK")
        return authcode
    # @profiler
    def getPlayerReport(self, start_date=Dates.today, end_date=Dates.today):
        self.__CheckUserLoginPassword__()
        self.__CheckForLogin__()
        auth_code = self.__Login__()
        response_data = self.api.GetClientTurnoverReportWithActiveBonus(auth_code, start_date, end_date)
        if response_data is None:
            return None
        return response_data.json()

    def getPlayerReportDayByDay(self, start_date: str, end_date: str) -> Generator[Optional[Dict[str, Any]], None, None]:
        current_date = datetime.strptime(start_date, '%d-%m-%y')
        end_date_obj = datetime.strptime(end_date, '%d-%m-%y')

        while current_date <= end_date_obj:
            self.__CheckUserLoginPassword__()
            self.__CheckForLogin__()
            auth_code = self.__Login__()
            date = current_date.strftime('%d-%m-%y')

            response_data = self.api.GetClientTurnoverReportWithActiveBonus(auth_code, date, date)
            if data := response_data if response_data else None:
                yield data.json(), current_date.date()
            else:
                yield None
            current_date += timedelta(days=1)

    @profiler
    def fill_db(self):
        # 250784 record 17-08-23 e kadar 15 dk
        # TODO: Pass no data dates
        # Copy from ile yapmayı dene db copy from'un bırakılan yerşden devam ettir.
        # hesaplamaları yaptır en son oluşan tabloları copy from ile insert et sonra oradan devam ettir.
        self.logger.info("Filling DB with data.")

        try:

            start_date = datetime.strptime(Dates.project_start_date, '%d-%m-%y').date()
            end_date = datetime.today().date() - timedelta(days=1)  # yesterday
            list_of_dates = create_date_list(start_date, end_date)


            for date in list_of_dates:
                date_str = date.strftime('%d-%m-%y')
                data = self.getPlayerReport(date_str, date_str)["Data"]

                if data is None or (isinstance(data, list) and len(data) == 0):
                    self.logger.info("No data for date: {}".format(date_str))
                    continue

                data_of_date_added = self.addDate(data, date)

                self.logger.info("Inserting data for date: {}".format(date_str))
                self.insertBulkPlayers(PlayersExceptToday, data_of_date_added)
        except Exception as e:
            raise e
    @profiler
    def download_data(self):

        gen = self.PlayersExceptTodayETL(Dates.project_start_date, Dates.yesterday)
        write_to_csv("./database/resources/data.csv.gz",  fieldnames=TableFields.PlayersExceptToday, generator=gen)




    def start(self):

        data = self.getPlayerReport(Dates.yesterday, Dates.yesterday)

        # self.download_data()

        self.crud.copyFromCSV(PlayersExceptToday, "./database/resources/data.csv")

        # Check if it is first run
        if validators.checkFirstRun():
            self.logger.info("First run detected")
            self.fill_db()
            self.logger.info("OK")
        else:
            self.logger.info("Not first run. Skipping DB filling. Cron will run as usual.")

    # def addDate(self, data, date):
    #     #formatted_data = [{'Date': date, 'Year': int(date[6:]), 'Month': int(date[3:5]), 'Day': int(date[:2]), **entry} for entry in data]
    #     formatted_data = [{'Date': date, 'Year': date.year, 'Month': date.month, 'Day': date.day, **entry} for entry in data]
    #     data = formatted_data
    #     return data

    def PlayersExceptTodayETL(self, start_date, end_date):
        for i, date in self.getPlayerReportDayByDay(start_date, end_date):
            data = i["Data"]
            if data is None or (isinstance(data, list) and len(data) == 0):
                continue

            formatted_data = [{'Date': date, 'Year': date.year, 'Month': date.month, 'Day': date.day, **entry} for entry in data]
            yield formatted_data

    def insertBulkPlayers(self, table, data_list: list):
        self.crud.insertData(table, data_list)
