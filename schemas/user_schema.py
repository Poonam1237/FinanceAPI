from pydantic import BaseModel,EmailStr

class UserData(BaseModel):
    name:str
    email:EmailStr
    password:str
    

class UserRespone(BaseModel):
    id:int
    name:str
    email:EmailStr
    role:str
    isactive:bool

    class Config:
        from_attributes=True

class UserLogin(BaseModel):
    email:str
    password:str
