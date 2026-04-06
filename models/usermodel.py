from sqlalchemy  import Column,Integer,String,Boolean
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100))
    email=Column(String(100))
    password=Column(String(255))
    role=Column(String(50))
    isactive=Column(Boolean,default=True)
    
    records=relationship("Records",back_populates="user")
