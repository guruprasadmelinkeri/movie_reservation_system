
from fastapi import FastAPI,APIRouter,Depends, HTTPException,Request

from sqlalchemy.orm import Session
from auth.rbac import create_admin, require
from database import get_db
from methods.show_method import get_user_tickets
from methods.user_method import create_user, verify_user,get_user
from schemas import CreateUser, GetCredentials

router=APIRouter()


@router.put("/user/add")
def user_create(credentials:CreateUser,db:Session=Depends(get_db)):
    return create_user(db,credentials)


@router.put("/admin/add")
def user_create(credentials:CreateUser,request:Request,db:Session=Depends(get_db)):
    token=request.session.get("access_token")
    if not token:
        raise HTTPException(status_code=404 , detail="please login first")
    user=get_user(db,request)

    require(user,"super")
    return create_admin(db,credentials)


@router.put("/user/verify")
def user_verify(credentials:GetCredentials,request:Request,db:Session=Depends(get_db)):
    return verify_user(db,request,credentials)

@router.get("/user/get")
def curr_user(request:Request,db:Session=Depends(get_db)):
    return get_user(db,request)

@router.get("/tickets")
def ticket_get(user_id:int,db:Session=Depends(get_db)):
    return get_user_tickets(db,user_id)
