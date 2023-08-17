from database.crud import Crud
from database.models import PlayersExceptToday
crud = Crud()


def checkFirstRun():
    return crud.checkDates(PlayersExceptToday)
