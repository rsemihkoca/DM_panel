from lib.api import Api
from lib.constants import Constants, Messages, Dates
from pprint import pprint
import time

import uvicorn
from database import models
from database.db import engine


models.Base.metadata.create_all(bind=engine)

app = create_app()

@app.get("/health")
async def healthy():
    return {"status": "healthy"}

    # api = Api()
    # print("CheckUserLoginPassword")
    # response_data = api.CheckUserLoginPassword()
    # print("CheckForLogin")
    # response_data = api.CheckForLogin()
    # print("Login")
    # response_data = api.Login()
    # authcode = response_data.headers['authentication']
    # if response_data:
    #     # print("==================header====================\n")
    #     # pprint(dict(response_data.headers))
    #     # print("==================response===================\n")
    #     # pprint(response_data.json())
    #     # print("==================authcode===================\n")
    #     pprint(authcode)
    #
    # print("GetClientTurnoverReportWithActiveBonus")
    #
    # start_time = time.time()
    #
    # response_data = api.GetClientTurnoverReportWithActiveBonus(authcode, Dates.today, Dates.today)
    #
    # end_time = time.time()
    #
    # elapsed_time = end_time - start_time
    #
    # if response_data:
    #     print("Elapsed time: ", elapsed_time)
    #     # print("==================header====================\n")
    #     # pprint(dict(response_data.headers))
    #     # print("==================response===================\n")
    #     pprint(response_data.json()["Data"])
    #     print("==================authcode===================\n")
    #     pprint(authcode)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)