from fastapi import APIRouter,Depends,HTTPException,status
from database import getdb
from sqlalchemy.orm import Session
from models.financialmodel import Records
from models.usermodel import User
from schemas.record_schema import RecordCreate,RecordResponse
from datetime import date
from auth.rbac import admin_required,analyst_required,viewer_required
router=APIRouter(prefix="/records",tags=["Records"])


@router.post("/create",response_model=RecordResponse,dependencies=[Depends(analyst_required)])
def create_record(request:RecordCreate,user:User=Depends(analyst_required),db:Session=Depends(getdb)):
    newrecord=Records(
       amt=request.amt,
       type=request.type,
       category=request.category,
       date=request.date,
       notes=request.notes,
       userid=user.id
    )

    db.add(newrecord)
    db.commit()
    db.refresh(newrecord)

    return newrecord

@router.get("/getrecord",response_model=list[RecordResponse],dependencies=[Depends(viewer_required)])
def get_records(db:Session=Depends(getdb)):
    records=db.query(Records).all()
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Records Found!")
    return records

@router.get("/getrecord/{id}",response_model=RecordResponse,dependencies=[Depends(viewer_required)])
def get_record(id:int,db:Session=Depends(getdb)):
    record=db.query(Records).filter(Records.id==id).first()

    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Record Not Found!")
    return record

@router.put("/update/{id}",response_model=RecordResponse,dependencies=[Depends(analyst_required)])
def update_records(id:int,request:RecordCreate,db:Session=Depends(getdb)):
    record=db.query(Records).filter(Records.id==id).first()

    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Record Not Found!")
    
    record.amt = request.amt
    record.type = request.type
    record.category = request.category
    record.date = request.date
    record.notes = request.notes

    db.commit()
    db.refresh(record)
    return record

@router.delete("/delete/{id}",dependencies=[Depends(admin_required)])
def delete_record(id:int,db:Session=Depends(getdb)):
    record=db.query(Records).filter(Records.id==id).first()

    if not record:
        return []
    
    db.delete(record)
    db.commit()
    return {"message":"Record Deleted Successfully!!"}


@router.get("/filter_record",response_model=list[RecordResponse],dependencies=[Depends(viewer_required)])
def filter_record(type:str=None,category:str=None,date:date=None,db:Session=Depends(getdb)):

    data=db.query(Records)

    if type:
        data=data.filter(Records.type==type)

    if category:
        data=data.filter(Records.category==category)

    if date:
        data=data.filter(Records.date==date)

    return data.all()
  
