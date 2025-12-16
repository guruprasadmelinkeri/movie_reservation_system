import os 
from dotenv import load_dotenv
from fastapi import HTTPException

from typing import Optional
from datetime import datetime,timedelta
from jose import  jwt
ALGORITHM="HS256"
load_dotenv(dotenv_path="../.env")
TOKEN_KEY=os.getenv("TOKEN_KEY")

if not TOKEN_KEY:
    raise HTTPException(status_code=404,detail="SECRET_KEY NOT FOUND")

def create_access_token(info:dict,expire:Optional[timedelta]=None):
    to_encode=info.copy()
    expires=datetime.utcnow()+(expire if expire else timedelta(days=1))

    to_encode.update({"exp":expires})
    encoded=jwt.encode(to_encode,key=TOKEN_KEY,algorithm=ALGORITHM)

    return encoded


def create_refresh_token(info:dict,expire:Optional[timedelta]=None):
    to_encode=info.copy()
    expires=datetime.utcnow()+(expire if expire else timedelta(days=7))

    to_encode.update({"exp":expires})
    encoded=jwt.encode(to_encode,key=TOKEN_KEY,algorithm=ALGORITHM)

    return encoded


