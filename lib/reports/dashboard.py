from database import models
from database.crud import Crud
import polars as pl
from lib.constants import Dates, CommissionCoefficients as CC
from lib.schemes.data import Schemas as SC
from typing import List, Dict
from datetime import datetime

CC = CC()
CC.CFK = 0.1
CC.SFK = 0.1
CC.FOK = 0.1
crud = Crud()

class DashboardCalculations:

    condition = (
        (pl.col('BTag').is_not_null()) &
        (pl.col('BTag') != "") &
        (
            (pl.col('BTag').str.lengths() == 6) |
            ((pl.col('BTag').str.lengths() == 7) & (pl.col('BTag') != "888692"))
        )
    )
    # ((df['BTag'].str.lengths() == 6) | ((df['BTag'].str.lengths() == 7) & (df['BTag'] != "888692")))
    # pl.col('Name').str.contains('William$').is_not()

    @staticmethod
    def GeneralSituation(data, *args):
        try:
            df = pl.DataFrame(data, schema=SC.dashboard)
            date = data[0]["Date"]

            CalculatedValues = DashboardCalculations.CalculateValues(df)
            DateAddedData = DashboardCalculations.AddDate(CalculatedValues, date)
            if datetime.strftime(date, '%d-%m-%y') == Dates.today:
                DashboardCalculations.DeleteData(table=models.GeneralSituationDashboard, date=date)
            DashboardCalculations.InsertData(data=DateAddedData, table=models.GeneralSituationDashboard)
        except Exception as e:
            print(e)

    @staticmethod
    def Affiliates(data, *args):
        """
        2021-10-01 : invalid series dtype: expected `Utf8`, got `bool` : schema = SC.dashboard
        :param data:
        :param args:
        :return:
        """
        try:

            df = pl.DataFrame(data, schema=SC.dashboard)
            date = data[0]["Date"]

            condition = DashboardCalculations.condition
            df = DashboardCalculations.FilterData(df, condition)
            CalculatedValues = DashboardCalculations.CalculateValues(df)
            DateAddedData = DashboardCalculations.AddDate(CalculatedValues, date)
            if datetime.strftime(date, '%d-%m-%y') == Dates.today:
                DashboardCalculations.DeleteData(table=models.AffiliateDashboard, date=date)
            DashboardCalculations.InsertData(data=DateAddedData, table=models.AffiliateDashboard)
        except Exception as e:
            print(e)

    @staticmethod
    def NaturalMembers(data, *args):
        try:
            df = pl.DataFrame(data, schema=SC.dashboard)
            date = data[0]["Date"]

            condition = ~DashboardCalculations.condition
            # ((df['BTag'].str.lengths() != 6) & (df['BTag'].str.lengths() != 7) | (df['BTag'] == "888692"))
            df = DashboardCalculations.FilterData(df, condition)
            CalculatedValues = DashboardCalculations.CalculateValues(df)
            DateAddedData = DashboardCalculations.AddDate(CalculatedValues, date)
            if datetime.strftime(date, '%d-%m-%y') == Dates.today:
                DashboardCalculations.DeleteData(table=models.NaturalMembersDashboard, date=date)
            DashboardCalculations.InsertData(data=DateAddedData, table=models.NaturalMembersDashboard)
        except Exception as e:
            print(e)

    @staticmethod
    def FilterData(df, condition):
        try:
            filtered_df = df.filter(condition)
        except Exception as e:
            print(e)
        else:
            return filtered_df

    @staticmethod
    def CalculateValues(df) -> List[dict]:
        try:
            # Deposits
            CountDeposit = df.filter(df["DepositCount"] > 0).shape[0]
            SumDepositAmount = df["DepositAmount"].sum()

            # Withdrawals
            WithdrawalCount = df.filter(df["WithdrawalCount"] > 0).shape[0]
            WithdrawalAmount = df["WithdrawalAmount"].sum()

            # Net Deposit
            NetDepositAmount = SumDepositAmount - WithdrawalAmount

            # Total Balance
            CountTotalBalance = df.filter(df["TotalBalance"] > 2).shape[0]
            SumTotalBalance = df.filter(df["TotalBalance"] > 2)["TotalBalance"].sum()

            # Sportsbook
            SumSportTotalBetAmount = df["SportTotalBetAmount"].sum()
            SumSportRealMoneyWonAmount = df["SportRealMoneyWonAmount"].sum()
            SportsBookInvoice = (SumSportTotalBetAmount - SumSportRealMoneyWonAmount) * CC.SFK

            # Casino
            SumCasinoTotalBetAmount = df["CasinoTotalBetAmount"].sum()
            SumCasinoRealMoneyWonAmount = df["CasinoRealMoneyWonAmount"].sum()
            CasinoInvoice = (SumCasinoTotalBetAmount - SumCasinoRealMoneyWonAmount) * CC.CFK

            # Total Commissions
            PaymentCommission = SumDepositAmount * CC.FOK
            AffiliateCommission = 0
            ProviderCommission = SportsBookInvoice + CasinoInvoice
            TotalInvoice = PaymentCommission + AffiliateCommission + ProviderCommission
        except Exception as e:
            print(e)
        else:
            return [{
                'CountDeposit': CountDeposit,
                'SumDepositAmount': SumDepositAmount,
                'WithdrawalCount': WithdrawalCount,
                'WithdrawalAmount': WithdrawalAmount,
                'NetDepositAmount': NetDepositAmount,
                'CountTotalBalance': CountTotalBalance,
                'SumTotalBalance': SumTotalBalance,
                'SumSportTotalBetAmount': SumSportTotalBetAmount,
                'SumSportRealMoneyWonAmount': SumSportRealMoneyWonAmount,
                'SportsBookInvoice': SportsBookInvoice,
                'SumCasinoTotalBetAmount': SumCasinoTotalBetAmount,
                'SumCasinoRealMoneyWonAmount': SumCasinoRealMoneyWonAmount,
                'CasinoInvoice': CasinoInvoice,
                'PaymentCommission': PaymentCommission,
                'AffiliateCommission': AffiliateCommission,
                'ProviderCommission': ProviderCommission,
                'TotalInvoice': TotalInvoice
            }]

    @staticmethod
    def AddDate(data, date):
        try:
            data[0]["Date"] = date
            data[0]["Year"] = date.year
            data[0]["Month"] = date.month
            data[0]["Day"] = date.day
        except Exception as e:
            print(e)
        else:
            return data

    @staticmethod
    def InsertData(data, table):
        try:
            crud.insertData(table=table, data=data)
        except Exception as e:
            print(e)

    @staticmethod
    def DeleteData(table, date):
        try:
            crud.deleteDate(table=table, date=date)
        except Exception as e:
            raise e