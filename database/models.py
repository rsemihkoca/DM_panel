from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Float
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from database.db import Base

class Players(Base):
    __tablename__ = 'Players'

    Date = Column(Date, primary_key=True)
    Year = Column(Integer, primary_key=True)
    Month = Column(Integer, primary_key=True)
    Day = Column(Integer, primary_key=True)
    ClientId = Column(Integer, primary_key=True)
    ClientName = Column(String)
    Login = Column(String)
    CurrencyId = Column(String)
    RegistrationDate = Column(DateTime)
    RegistrationDateLocal = Column(DateTime)
    SportsbookProfileId = Column(Integer)
    CurrentBalance = Column(Float)
    BTag = Column(String)
    AffilateId = Column(String)
    AcceptanceDateLocal = Column(DateTime)
    ExpirationDateLocal = Column(DateTime)
    ResultDateLocal = Column(DateTime)
    SportBetAmount = Column(Float)
    SportBetCount = Column(Integer)
    CasinoBetAmount = Column(Float)
    SportBonusBetAmount = Column(Float)
    CasinoBonusBetAmount = Column(Float)
    SportBonusWinAmount = Column(Float)
    CasinoBonusWinAmount = Column(Float)
    SportBonusAmount = Column(Float)
    CasinoBonusAmount = Column(Float)
    ActiveBonusAmount = Column(Float)
    ActiveBonusType = Column(Integer)
    PlayerType = Column(Integer)
    SumBonusBalance = Column(Float)
    TotalBalance = Column(Float)
    SportNetProfit = Column(Float)
    CasinoNetProfit = Column(Float)
    SportNetProfitLessBonus = Column(Float)
    CasinoNetProfitLessBonus = Column(Float)
    SportTotalBetAmount = Column(Float)
    CasinoTotalBetAmount = Column(Float)
    SportRealMoneyWonAmount = Column(Float)
    CasinoRealMoneyWonAmount = Column(Float)
    CasinoBetCount = Column(Integer)
    NetProfit = Column(Float)
    NetProfitLessBonus = Column(Float)
    RealMoneyBetAmount = Column(Float)
    BonusBetAmount = Column(Float)
    TotalBetAmount = Column(Float)
    RealMoneyWonAmount = Column(Float)
    BonusWonAmount = Column(Float)
    ConvertedBonusAmount = Column(Float)
    DepositAmount = Column(Float)
    DepositCount = Column(Integer)
    WithdrawalAmount = Column(Float)
    WithdrawalCount = Column(Integer)
    IsVerified = Column(Boolean)
    PeriodStartBalance = Column(Float)
    PeriodEndBalance = Column(Float)
    CasinoPeriodStartBalance = Column(Float)
    CasinoPeriodEndBalance = Column(Float)

    @classmethod
    def get_column_names(cls):
        # Use the declared attributes to get columns and filter out anything that's not a column
        return [key for key, column in cls.__dict__.items() if isinstance(column, InstrumentedAttribute)]



class GeneralSituationDashboard(Base):

    __tablename__ = 'GeneralSituationDashboard'

    Date = Column(Date, primary_key=True)
    Year = Column(Integer, primary_key=True)
    Month = Column(Integer, primary_key=True)
    Day = Column(Integer, primary_key=True)

    # Yatirim
    CountDeposit = Column(Integer)
    SumDepositAmount = Column(Float)

    # Cekim
    WithdrawalCount = Column(Integer)
    WithdrawalAmount = Column(Float)

    # Yatirim - Cekim
    NetDepositAmount = Column(Float)

    # Total Balance
    CountTotalBalance = Column(Float)
    SumTotalBalance = Column(Float)

    # FATURALAR

    # Sportsbook
    SumSportTotalBetAmount = Column(Float)
    SumSportRealMoneyWonAmount = Column(Float)
    SportsBookInvoice = Column(Float)

    # Casino
    SumCasinoTotalBetAmount = Column(Float)
    SumCasinoRealMoneyWonAmount = Column(Float)
    CasinoInvoice = Column(Float)

    # Toplam
    PaymentCommission = Column(Float)
    AffiliateCommission = Column(Float)
    ProviderCommission = Column(Float)
    TotalInvoice = Column(Float)

    @classmethod
    def get_column_names(cls):
        # Use the declared attributes to get columns and filter out anything that's not a column
        return [key for key, column in cls.__dict__.items() if isinstance(column, InstrumentedAttribute)]


class AffiliateDashboard(Base):

    __tablename__ = 'AffiliateDashboard'

    Date = Column(Date, primary_key=True)
    Year = Column(Integer, primary_key=True)
    Month = Column(Integer, primary_key=True)
    Day = Column(Integer, primary_key=True)

    # Yatirim
    CountDeposit = Column(Integer)
    SumDepositAmount = Column(Float)

    # Cekim
    WithdrawalCount = Column(Integer)
    WithdrawalAmount = Column(Float)

    # Yatirim - Cekim
    NetDepositAmount = Column(Float)

    # Total Balance
    CountTotalBalance = Column(Float)
    SumTotalBalance = Column(Float)

    # FATURALAR

    # Sportsbook
    SumSportTotalBetAmount = Column(Float)
    SumSportRealMoneyWonAmount = Column(Float)
    SportsBookInvoice = Column(Float)

    # Casino
    SumCasinoTotalBetAmount = Column(Float)
    SumCasinoRealMoneyWonAmount = Column(Float)
    CasinoInvoice = Column(Float)

    # Toplam
    PaymentCommission = Column(Float)
    AffiliateCommission = Column(Float)
    ProviderCommission = Column(Float)
    TotalInvoice = Column(Float)

    @classmethod
    def get_column_names(cls):
        # Use the declared attributes to get columns and filter out anything that's not a column
        return [key for key, column in cls.__dict__.items() if isinstance(column, InstrumentedAttribute)]

class NaturalMembersDashboard(Base):

    __tablename__ = 'NaturalMembersDashboard'

    Date = Column(Date, primary_key=True)
    Year = Column(Integer, primary_key=True)
    Month = Column(Integer, primary_key=True)
    Day = Column(Integer, primary_key=True)

    # Yatirim
    CountDeposit = Column(Integer)
    SumDepositAmount = Column(Float)

    # Cekim
    WithdrawalCount = Column(Integer)
    WithdrawalAmount = Column(Float)

    # Yatirim - Cekim
    NetDepositAmount = Column(Float)

    # Total Balance
    CountTotalBalance = Column(Float)
    SumTotalBalance = Column(Float)

    # FATURALAR

    # Sportsbook
    SumSportTotalBetAmount = Column(Float)
    SumSportRealMoneyWonAmount = Column(Float)
    SportsBookInvoice = Column(Float)

    # Casino
    SumCasinoTotalBetAmount = Column(Float)
    SumCasinoRealMoneyWonAmount = Column(Float)
    CasinoInvoice = Column(Float)

    # Toplam
    PaymentCommission = Column(Float)
    AffiliateCommission = Column(Float)
    ProviderCommission = Column(Float)
    TotalInvoice = Column(Float)

    @classmethod
    def get_column_names(cls):
        # Use the declared attributes to get columns and filter out anything that's not a column
        return [key for key, column in cls.__dict__.items() if isinstance(column, InstrumentedAttribute)]



class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
