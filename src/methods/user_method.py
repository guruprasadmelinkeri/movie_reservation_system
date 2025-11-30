from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user_model import User
from schemas import CreateUser,GetCredentials
from auth.hashing import hash,verify



def create_user(db:Session,credentials:CreateUser):
    user=db.query(User).filter(User.username==credentials.Username).first()
    if user:
        raise HTTPException(status_code=300,detail="user exists")
    new_user=User(
        username=credentials.Username,
        hashed_password=hash(credentials.Password)
    )

    db.add(new_user)
    db.commit()

    return {new_user.username}


def verify_user(db:Session,credentials:GetCredentials):
    user=db.query(User).filter(User.username==credentials.Username).first()
    if not user:
        raise HTTPException(status_code=300,detail="user not found")
    
    

    return verify(hashed=user.hashed_password,password=credentials.Password)