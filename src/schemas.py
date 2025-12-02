
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
    

class CreateShowItem(BaseModel):
    user_id:int
    show_id:int

class CreateShowItemSeat(BaseModel):
    show_item_id:int
    seat_id:int

class CreateSeat(BaseModel):
    screen_id:int
    seat_name:str
    price:int


class CreateShow(BaseModel):
    screen_id:int
    movie_name:str
    start_time:datetime
    end_time:datetime