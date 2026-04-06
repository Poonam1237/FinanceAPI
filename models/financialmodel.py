from sqlalchemy import Column,Integer,String,Float,Date,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Records(Base):
    __tablename__="financial_records"
    id=Column(Integer,primary_key=True,index=True)
    amt=Column(Float)
    type=Column(String(50))
    category=Column(String(50))
    date=Column(Date)
    notes=Column(String(225))
    userid=Column(Integer,ForeignKey("users.id"))

    user=relationship("User",back_populates="records")

