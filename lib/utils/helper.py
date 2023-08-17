import time
import datetime


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
    # date_list = []
    # current_date = datetime.datetime.strptime(start_date, '%d-%m-%y')
    # end_date = datetime.datetime.strptime(end_date, '%d-%m-%y')
    # while current_date <= end_date:
    #     date_list.append(current_date.strftime('%d-%m-%y'))
    #     current_date += datetime.timedelta(days=1)
    #
    # return date_list

