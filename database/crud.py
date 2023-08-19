from sqlalchemy.orm.decl_api import DeclarativeMeta
from database.db import SessionLocal, engine
from database.models import PlayersExceptToday, PlayersToday
from lib.constants import TableFields
import postgres_copy

class Crud:

    def checkDates(self, table: type(DeclarativeMeta)):
        with SessionLocal() as session:
            try:
                date = session.query(table).count()

                if date == 0:
                    return True
                return False

            except Exception as e:
                raise e
    def insertData(self, table: type(DeclarativeMeta), data: list):
        with SessionLocal() as session:
            try:
                session.bulk_insert_mappings(table, data)
                session.commit()

            except Exception as e:
                session.rollback()
                raise e

    def copyFromCSV(self, table: type(DeclarativeMeta), path: str):
            with open(path) as fp:
                try:
                    # columns = getattr(TableFields, table.__name__)
                    postgres_copy.copy_from(fp, table, engine, format='csv', delimiter=',', header=True, null='')

                except Exception as e:
                    raise e
