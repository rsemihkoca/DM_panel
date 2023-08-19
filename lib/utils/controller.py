import logging
from lib.api import Api
from lib.asyncapi import AsyncAPI
from lib.constants import Dates, Dates, TableFields
from lib.utils.helper import profiler, create_date_list, write_to_csv
from lib.utils import validators
from database.crud import Crud
from database import models
from logging.handlers import RotatingFileHandler
from lib.pipeline import Pipeline
from lib.reports.dashboard import DasboardCalculations
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
        self.async_api = AsyncAPI()
        self.logger = logger
        self.crud = Crud()
    # @profiler

    @profiler
    def download_data(self):
        gen = self.api.PlayersETL(Dates.project_start_date, Dates.yesterday)
        write_to_csv("./database/resources/data.csv.gz",  fieldnames=TableFields.Players, generator=gen)




    def start(self):

        threads = [
            (self.insertBulkPlayers, models.Players),
            (DasboardCalculations.General, 'arg1'),
            (DasboardCalculations.General, 'arg1'),
            (func2, 'arg2')]
        processor = Pipeline(self.async_api.PlayersETL(Dates.project_start_date, Dates.yesterday), threads)
        processor.start()

        data = self.api.getPlayerReport(Dates.yesterday, Dates.yesterday)

        # self.download_data()

        self.crud.copyFromCSV(models.Players, "./database/resources/data.csv")

        # Check if it is first run
        if validators.checkFirstRun():
            self.logger.info("First run detected")
            self.logger.info("OK")
        else:
            self.logger.info("Not first run. Skipping DB filling. Cron will run as usual.")


    def insertBulkPlayers(self, table, data: list):
        self.crud.insertData(table, data)
