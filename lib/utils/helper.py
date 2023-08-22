import gzip, csv
import time
import datetime

current_day = datetime.datetime.now().date()
def profiler(func):
    """
    A decorator that prints the time a function takes
    to execute.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {(end_time - start_time):.5f} seconds")
        return result
    return wrapper

def create_date_list(start_date, end_date):
    return [(start_date + datetime.timedelta(days=i)) for i in range((end_date - start_date).days + 1)]


def write_to_csv(directory_name, fieldnames, generator):
    rows = []
    try:
        with gzip.open(directory_name, 'wt', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for row in generator:
                rows.extend(row)
                if len(rows) >= 10_000:
                    writer.writerows(rows)
                    rows = []
                    csvfile.flush()  # flush the buffer to ensure data is written to disk
            if len(rows) > 0:
                writer.writerows(rows)
                csvfile.flush()
        return True
    except Exception as e:
        del rows
        raise e

def has_day_changed():
    global current_day
    today = datetime.datetime.now().date()
    if today != current_day:
        current_day = today
        print("Day has changed.")
        return True
    return False