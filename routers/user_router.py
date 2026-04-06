from fastapi import APIRouter,Depends,HTTPException,status
from database import getdb
from sqlalchemy.orm import Session
from  models.usermodel import User
from schemas.user_schema import UserData,UserRespone,UserLogin
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from auth.createtoken import create_token
from auth.rbac import admin_required,viewer_required

router=APIRouter(prefix="/users",tags=["Users"])

pwd=CryptContext(schemes=['bcrypt'],deprecated="auto")

@router.post("/register",response_model=UserRespone)
def register(request:UserData,db:Session=Depends(getdb)):
    existing=db.query(User).filter(User.email==request.email).first()

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists!")

    newuser=User(
        name=request.name,
        email=request.email,
        password=pwd.hash(request.password),
        role="viewer"
    )

    db.add(newuser)
    db.commit()
    db.refresh(newuser)

    return newuser

@router.post("/login")
def login(request:UserLogin,db:Session=Depends(getdb)):
    user=db.query(User).filter(request.email==User.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No User Found!")

    verifypwd=pwd.verify(request.password, user.password)
    if not verifypwd:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Password!")

    data={"sub":user.email,"role":user.role}
    get_token=create_token(data)
    return {
        "access_token":get_token,
        "token_type": "bearer"
    }


@router.get("/getdata",response_model=list[UserRespone],dependencies=[Depends(admin_required)])
def getusers(db:Session=Depends(getdb)):
    users=db.query(User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No User Found!")
    return users

@router.get("/getdata/{id}",response_model=UserRespone)
def getuser(id:int,db:Session=Depends(getdb),current_user=Depends(viewer_required)):

    if current_user.role == "viewer":
        if id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No access to other users' data")
    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found!")
    return user


@router.put("/update/{id}",response_model=UserRespone,dependencies=[Depends(admin_required)])
def update_user(id:int,request:UserData,db:Session=Depends(getdb)):
    user=db.query(User).filter(User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found!")
    
    user.name = request.name
    user.email = request.email
    user.password = pwd.hash(request.password)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/delete/{id}",dependencies=[Depends(admin_required)])
def delete_user(id:int,db:Session=Depends(getdb)):
    user=db.query(User).filter(User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found!")
    
    db.delete(user)
    db.commit()
    return {"message":"User Data Deleted Successfully!!"}


@router.post("/changerole/{id}",dependencies=[Depends(admin_required)])
def changerole(id, db: Session = Depends(getdb)):
    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found!")

    user.role="analyst"
    db.commit() 
    db.refresh(user)
    return {"message":"Role updated from viewer to analyst successfully!"}

