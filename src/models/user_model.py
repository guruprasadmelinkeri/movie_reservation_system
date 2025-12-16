
from sqlalchemy import Column, Integer,String,ForeignKey,DateTime,Boolean, column
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer,unique=True,index=True,primary_key=True)
    username=Column(String,unique=True, nullable=False)
    email=Column(String,unique=True)
    hashed_password=Column(String , nullable=False)
    tickets=relationship("ShowItem")
    refresh_token=relationship("RefreshToken",back_populates="user",cascade="all ,delete")


class RefreshToken(Base):
    __tablename__="refresh_tokens"
    id=Column(Integer,unique=True,index=True,primary_key=True)
    token=Column(String ,nullable=False)
    user_id=Column(ForeignKey("users.id"))
    is_revoked=Column(Boolean,default=False)
    expires_at=Column(DateTime)
    user=relationship("User",back_populates="refresh_token")