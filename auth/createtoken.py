from auth.my_http_bearer import myhttpbearer
from fastapi import HTTPException,Depends
from models.usermodel import User

bearer=myhttpbearer()
def admin_required(current_user:User=Depends(bearer)):

    if (current_user.role).lower()!="admin":
        raise HTTPException(status_code=403,detail="Admin privileges required")
    return current_user

def analyst_required(current_user:User=Depends(bearer)):
    if (current_user.role).lower() not in ["admin", "analyst"]:
        raise HTTPException(status_code=403, detail="Analyst privileges required") 
    return current_user

def viewer_required(current_user:User=Depends(bearer)):
       return current_user
