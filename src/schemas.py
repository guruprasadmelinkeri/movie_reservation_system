
from pydantic import BaseModel
from sqlalchemy import JSON
from datetime import datetime
from typing import List


class CreateUser(BaseModel):
    Username:str
    Password:str

class GetCredentials(BaseModel):
    Username:str
    Password:str

class CreateScreen(BaseModel):
    Number:int
    all_seats:List[str]

class CreateShowItem(BaseModel):
    show_id:int
    seats:List[str]
    quantity:int
    price:int

class CreateSeat(BaseModel):
    screen_id:int
    show_id:int
    available_seats:List[str]
    booked_seats:List[str]
    price:int


class CreateShow(BaseModel):
    screen_id:int
    movie_name:str
    start_time:datetime
    end_time:datetime