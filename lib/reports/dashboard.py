from database import models
from database.crud import Crud
import polars as pl
from lib.constants import CommissionCoefficients as CC
from typing import List, Dict

class DasbhoardCalculations:

    @staticmethod
    def GeneralSituation(data):
        df = pl.DataFrame(data)

        CalculatedValues = DasbhoardCalculations.CalculateValues(df)
        DasbhoardCalculations.InsertData(models.GeneralSituationDashboard, CalculatedValues)


    @staticmethod
    def Affiliates(data):
        df = pl.DataFrame(data)

        df = DasbhoardCalculations.FilterAffiliates(df)
        CalculatedValues = DasbhoardCalculations.CalculateValues(df)
        DasbhoardCalculations.InsertData(models.GeneralSituationDashboard, CalculatedValues)
    @staticmethod
    def NaturalMembers(data):
        df = pl.DataFrame(data)

        df = DasbhoardCalculations.FilterNaturalMembers(df)
        CalculatedValues = DasbhoardCalculations.CalculateValues(df)
        DasbhoardCalculations.InsertData(models.GeneralSituationDashboard, CalculatedValues)

    @staticmethod
    def FilterAffiliates(df):
        df.filter((df['BTag'].str.len() == 6) | (df['BTag'].str.len() == 7) & (df['BTag'] != "888692"))
        return df
    @staticmethod
    def FilterNaturalMembers(df):
        df.filter((df['BTag'].str.len() != 6) & (df['BTag'].str.len() != 7) | (df['BTag'] == "888692"))
        return df
    @staticmethod
    def CalculateValues(df) -> List[dict]:

        # Deposits
        CountDeposit = df.filter(df["DepositCount"] > 0).shape[0]
        SumDepositAmount = df["DepositAmount"].sum().get()

        # Withdrawals
        WithdrawalCount = df.filter(df["WithdrawalCount"] > 0).shape[0]
        WithdrawalAmount = df["WithdrawalAmount"].sum().get()

        # Net Deposit
        NetDepositAmount = SumDepositAmount - WithdrawalAmount

        # Total Balance
        CountTotalBalance = df.filter(df["TotalBalance"] > 2).shape[0]
        SumTotalBalance = df.filter(df["TotalBalance"] > 2)["TotalBalance"].sum().get()

        # Sportsbook
        SumSportTotalBetAmount = df["SportTotalBetAmount"].sum().get()
        SumSportRealMoneyWonAmount = df["SportRealMoneyWonAmount"].sum().get()
        SportsBookInvoice = (SumSportTotalBetAmount - SumSportRealMoneyWonAmount) * CC.SFK

        # Casino
        SumCasinoTotalBetAmount = df["CasinoTotalBetAmount"].sum().get()
        SumCasinoRealMoneyWonAmount = df["CasinoRealMoneyWonAmount"].sum().get()
        CasinoInvoice = (SumCasinoTotalBetAmount - SumCasinoRealMoneyWonAmount) * CC.CFK

        # Total Commissions
        PaymentCommission = SumDepositAmount * CC.FOK
        AffiliateCommission = 0
        ProviderCommission = SportsBookInvoice + CasinoInvoice
        TotalInvoice = PaymentCommission + AffiliateCommission + ProviderCommission

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
    def InsertData(table, data):
        Crud.insertData(table, data)

