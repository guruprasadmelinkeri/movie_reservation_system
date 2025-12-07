
from fastapi import FastAPI,APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from methods.show_method import get_user_tickets
from methods.user_method import create_user, verify_user
from schemas import CreateUser, GetCredentials

router=APIRouter()


@router.put("/user/add")
def user_verify(credentials:CreateUser,db:Session=Depends(get_db)):
    return create_user(db,credentials)


@router.put("/user/verify")
def user_verify(credentials:GetCredentials,db:Session=Depends(get_db)):
    return verify_user(db,credentials)

@router.get("/tickets")
def ticket_get(user_id:int,db:Session=Depends(get_db)):
    return get_user_tickets(db,user_id)
