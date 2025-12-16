
import datetime

from fastapi import HTTPException,Request

from jose import JWTError,ExpiredSignatureError,jwt
from sqlalchemy.orm import Session
from auth.tokens import create_access_token, create_refresh_token
from models.user_model import RefreshToken, User
from schemas import CreateUser,GetCredentials
from auth.hashing import hash,verify
from auth.tokens import TOKEN_KEY,ALGORITHM


def create_user(db:Session,credentials:CreateUser):
    user=db.query(User).filter(User.email==credentials.email).first()
    if user:
        raise HTTPException(status_code=300,detail="user exists")
    new_user=User(
        username=credentials.Username,
        email=credentials.email,
        hashed_password=hash(credentials.Password)
    )

    db.add(new_user)
    db.commit()

    return {new_user.username}


def verify_user(db:Session,request:Request,credentials:GetCredentials):
    user=db.query(User).filter(User.username==credentials.Username ).first()
    if not user:
        raise HTTPException(status_code=300,detail="user not found")
    
    if(verify(hashed=user.hashed_password,password=credentials.Password)):

        access_token =create_access_token({"sub":user.email})
        refresh_token=create_refresh_token({"sub":user.email})

        new_token=RefreshToken(
            expires_at=datetime.datetime.now()+datetime.timedelta(days=7),
            user_id=user.id,
            is_revoked=False,
            token=refresh_token

        )

        db.add(new_token)
        db.commit()

        request.session["access_token"]=access_token

        return {"status_code":200}
    
    

    raise HTTPException(status_code=404,detail="wrong credentials")


def refresh_access_token(db:Session,request:Request,email:str):
    user=db.query(User).filter(User.email==email ).first()
    if not user:
        raise HTTPException(status_code=300,detail="user not found")
    token=db.query(RefreshToken).filter(RefreshToken.user_id==user.id,
                                        RefreshToken.expires_at>datetime.datetime.utcnow(),
                                        RefreshToken.is_revoked==False).order_by(RefreshToken.id.desc()).first()
    
    if not token:
        raise HTTPException(status_code=404, detail="please login again")
    
    token.is_revoked=True

    access_token=create_access_token({"sub":user.email},datetime.timedelta(days=1))
    refresh_token=create_refresh_token({"sub":user.email},datetime.timedelta(days=7))

    new_token=RefreshToken(
            expires_at=datetime.datetime.now()+datetime.timedelta(days=7),
            user_id=user.id,
            is_revoked=False,
            token=refresh_token

        )

    db.add(new_token)
    db.commit()

    request.session["access_token"]=access_token

    return user

def get_user(db:Session,request:Request):
    try:
        token=request.session.get("access_token")
        payload=jwt.decode(token,TOKEN_KEY,algorithms=ALGORITHM)
        email=payload.get("sub")
        user=db.query(User).filter(User.email==email).first()
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        return user
    except ExpiredSignatureError:
        token=request.session.get("access_token")
        payload=jwt.decode(token,TOKEN_KEY,algorithms=ALGORITHM)
        email=payload.get("sub")
        user=refresh_access_token(db,request,email)
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        return user

        
        


    except JWTError:
        raise HTTPException(status_code=404, detail="please login again")