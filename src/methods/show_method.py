import json
from fastapi import HTTPException
from models.screen_models import Screen,Seat,ShowItem
from sqlalchemy.orm import Session

from schemas import CreateScreen, CreateSeat, CreateShowItem


def create_screen(db:Session,screen:CreateScreen):
    new_screen=db.query(Screen).filter(Screen.number==screen.Number).first()
    if new_screen:
        raise HTTPException(status_code=400,detail="screen number taken")
    new_screen=Screen(
        number=screen.Number,
        seat_id=screen.seat_id,
        
    )
    db.add(new_screen)
    db.commit()

    return new_screen

def create_show_item(db:Session,item:CreateShowItem):
    
    new_item=ShowItem(
        screen_id=item.screen_id,
        quantity=item.quantity,
        seats=item.quantity
        
    )
    db.add(new_item)
    db.commit()

    return new_item

def create_seats(db:Session,seat:CreateSeat):
    new_seat=db.query(Seat).filter(Seat.screen_id==seat.screen_id).first()

    if new_seat:
        raise HTTPException(status_code=400,detail="seats exist for given screen")
    new_seat=Seat(
        available_seats=seat.available_seats,
        booked_seats=seat.booked_seats,
        price=seat.price,
        screen_id=seat.screen_id
    )
    db.add(new_seat)
    db.commit()

    return {"available_seats":new_seat.available_seats,"screen_id":new_seat.screen_id}


def get_all_screens(db:Session):
    return db.query(Screen).all()

def get_screen_seats(db:Session,Number:int):
    screen=db.query(Screen).filter(Screen.number==Number).first()

    if not screen:
        raise HTTPException(status_code=400,detail="screen not found")
    
  
    return screen.seats