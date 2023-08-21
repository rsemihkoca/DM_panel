from sqlalchemy.orm.decl_api import DeclarativeMeta
from database.db import SessionLocal, engine, Base
from database.models import Players
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

    def deleteTables(self):
        with SessionLocal() as session:
            try:
                # Iterate through tables sorted by their dependencies
                for table in reversed(Base.metadata.sorted_tables):
                    session.execute(table.delete())

                session.commit()

            except Exception as e:
                print("An error occurred:", e)
                session.rollback()
                raise e
            finally:
                session.close()
                return True
    def copyFromCSV(self, table: type(DeclarativeMeta), path: str):
            with open(path) as fp:
                try:
                    # columns = getattr(TableFields, table.__name__)
                    postgres_copy.copy_from(fp, table, engine, format='csv', delimiter=',', header=True, null='')

                except Exception as e:
                    raise e
