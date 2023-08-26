import logging, asyncio
from datetime import datetime
from lib.api import Api
from lib.asyncapi import AsyncAPI
from lib.constants import Dates, TableFields
from lib.config import Config
from lib.utils.helper import profiler, write_to_csv
from lib.utils import validators
from database.crud import Crud
from database import models
from logging.handlers import RotatingFileHandler
from lib.utils.pipeline import Pipeline
from lib.reports.dashboard import DashboardCalculations as DC

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



    @profiler
    def start(self):

        # data = self.api.getPlayerReport(Dates.yesterday, Dates.yesterday)
        """
        YENI GUNE GECILDIGINDE DUNE AIT VERI DOGRU OLMALI !!!!

        VERI KALITE KONTROLU yapmaya devam et

        Önce flow: bunun için go ile mikroservis yazar ortaya broker koyarız
        ardından fastapi istekleri

        """
        # if self.crud.deleteTables():
        #     self.logger.info("Tables deleted successfully")

        print("STARTED AT:", datetime.now())
        threads = (
            (self.insertBulkPlayers, models.Players),
            (DC.GeneralSituation, None),
            (DC.Affiliates, None),
            (DC.NaturalMembers, None)
        )

        # etl = self.async_api.PlayersETL(Dates.project_start_date, Dates.yesterday, cron=False)

        # etl = self.async_api.PlayersETL(Dates.last_7_days, Dates.yesterday, cron=False)
        # processor = Pipeline(etl, threads)
        # asyncio.run(processor.start())
        # self.logger.info("ETL process completed successfully")
        # print("FINISHED AT:", datetime.now())

        generator = self.async_api.PlayersETL(Dates.today, Dates.today, cron=True)
        async_cron_job = self.async_api.run_cron(generator, Config.refresh_interval)
        processor = Pipeline(async_cron_job, threads)
        asyncio.run(processor.start())

    def insertBulkPlayers(self, data, table: list):
        date = data[0]["Date"]
        if datetime.strftime(date, '%d-%m-%y') == Dates.today:
            self.crud.deleteDate(table, date)
        self.crud.insertData(table, data)

