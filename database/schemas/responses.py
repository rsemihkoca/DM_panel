from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import JSONResponse



class SuccessCreateResponse(BaseModel):
    data: int