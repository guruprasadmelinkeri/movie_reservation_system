
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user_model import User
from auth.hashing import hash
import os
import dotenv

from schemas import CreateUser

dotenv.load_dotenv('../.env')

def require(user:User, *roles):
    if user.role not in roles:
        raise HTTPException(status_code=400 , detail="access denied")

def create_admin(db:Session,credentials:CreateUser):
    admin=User(
        hashed_password=hash(credentials.Password),
        email=credentials.email,
        role="admin",
        username=credentials.Username,
        

    )

    db.add(admin)
    db.commit()



def create_super(db:Session,username:str,email:str,password:str):
    admin=User(
        hashed_password=hash(password),
        email=email,
        role="super",
        username=username,
        

    )

    db.add(admin)
    db.commit()




