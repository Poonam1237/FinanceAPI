from pydantic import BaseModel
from datetime import date

class RecordCreate(BaseModel):
    amt:float
    type:str
    category:str
    date:date
    notes:str

class RecordResponse(BaseModel):
    id:int
    amt:float
    type:str
    category:str
    date:date
    notes:str
    class Config:
        from_attributes=True