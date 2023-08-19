from database.crud import Crud
from database.models import Players
crud = Crud()


def checkFirstRun():
    return crud.checkDates(Players)
