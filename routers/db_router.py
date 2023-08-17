from fastapi import APIRouter, UploadFile, File, Form, Query, Depends
from starlette.requests import Request
from database.schemas.responses import SuccessCreateResponse
#from database.schemas.parameters import

router = APIRouter()

@router.post("", summary="Used for extract and insert all data", response_model=SuccessCreateResponse)
def reset(request: Request):

    try:
        count= request.app.controller.reset()
        return SuccessCreateResponse(data=count)
    except Exception as e:
        raise e