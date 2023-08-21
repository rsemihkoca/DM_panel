import polars as pl

class Schemas:
    dashboard = {
        'Date': pl.Date,
        'Year': pl.Int64,
        'Month': pl.Int64,
        'Day': pl.Int64,
        'ClientId': pl.Int64,
        'ClientName': pl.Utf8,
        'Login': pl.Utf8,
        'CurrencyId': pl.Utf8,
        'RegistrationDate': pl.Utf8,
        'RegistrationDateLocal': pl.Utf8,
        'SportsbookProfileId': pl.Int64,
        'CurrentBalance': pl.Float64,
        'BTag': pl.Utf8,  # Updated
        'AffilateId': pl.Utf8,  # Updated
        'AcceptanceDateLocal': pl.Utf8,  # Updated
        'ExpirationDateLocal': pl.Utf8,  # Updated
        'ResultDateLocal': pl.Utf8,  # Updated
        'SportBetAmount': pl.Float64,
        'SportBetCount': pl.Int64,
        'CasinoBetAmount': pl.Float64,
        'SportBonusBetAmount': pl.Float64,
        'CasinoBonusBetAmount': pl.Float64,
        'SportBonusWinAmount': pl.Float64,
        'CasinoBonusWinAmount': pl.Float64,
        'SportBonusAmount': pl.Float64,
        'CasinoBonusAmount': pl.Float64,
        'ActiveBonusAmount': pl.Utf8,  # Updated
        'ActiveBonusType': pl.Utf8,  # Updated
        'PlayerType': pl.Int64,
        'SumBonusBalance': pl.Float64,
        'TotalBalance': pl.Float64,
        'SportNetProfit': pl.Float64,
        'CasinoNetProfit': pl.Float64,
        'SportNetProfitLessBonus': pl.Float64,
        'CasinoNetProfitLessBonus': pl.Float64,
        'SportTotalBetAmount': pl.Float64,
        'CasinoTotalBetAmount': pl.Float64,
        'SportRealMoneyWonAmount': pl.Float64,
        'CasinoRealMoneyWonAmount': pl.Float64,
        'CasinoBetCount': pl.Int64,
        'NetProfit': pl.Float64,
        'NetProfitLessBonus': pl.Float64,
        'RealMoneyBetAmount': pl.Float64,
        'BonusBetAmount': pl.Float64,
        'TotalBetAmount': pl.Float64,
        'RealMoneyWonAmount': pl.Float64,
        'BonusWonAmount': pl.Float64,
        'ConvertedBonusAmount': pl.Float64,
        'DepositAmount': pl.Float64,
        'DepositCount': pl.Float64,
        'WithdrawalAmount': pl.Float64,
        'WithdrawalCount': pl.Float64,
        'IsVerified': pl.Boolean,
        'PeriodStartBalance': pl.Float64,
        'PeriodEndBalance': pl.Float64,
        'CasinoPeriodStartBalance': pl.Float64,
        'CasinoPeriodEndBalance': pl.Float64
    }