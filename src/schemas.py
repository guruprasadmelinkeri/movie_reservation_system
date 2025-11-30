from pydantic import BaseModel
from sqlalchemy import JSON
from typing import List


class CreateUser(BaseModel):
    Username:str
    Password:str

class GetCredentials(BaseModel):
    Username:str
    Password:str

class CreateScreen(BaseModel):
    Number:int
    seat_id:int

class CreateShowItem(BaseModel):
    screen_id:int
    seats:List[str]
    quantity:int
    price:int

class CreateSeat(BaseModel):
    screen_id:int
    available_seats:List[str]
    booked_seats:List[str]
    price:int