from sqlalchemy.orm.decl_api import DeclarativeMeta
from database.db import SessionLocal, engine
from database.models import PlayersExceptToday, PlayersToday

class Crud:

    def checkDates(self, table: DeclarativeMeta):
        with SessionLocal() as session:
            try:
                date = session.query(table).filter(PlayersExceptToday.Date.is_(None)).all()

                if date is None or (isinstance(date, list) and len(date) == 0):
                    return True
                return False

            except Exception as e:
                raise e
    def insertData(self, table: DeclarativeMeta, data: list):
        with SessionLocal() as session:
            try:
                session.bulk_insert_mappings(table, data)
                session.commit()

            except Exception as e:
                session.rollback()
                raise e
