
import json
from fastapi import HTTPException
from models.screen_models import Screen,Seat,ShowItem,Show
from sqlalchemy.orm import Session

from schemas import CreateScreen, CreateSeat, CreateShow, CreateShowItem


def create_screen(db:Session,screen:CreateScreen):
    new_screen=db.query(Screen).filter(Screen.number==screen.Number).first()
    if new_screen:
        raise HTTPException(status_code=400,detail="screen number taken")
    new_screen=Screen(
        number=screen.Number,
        all_seats=screen.all_seats
        
    )
    db.add(new_screen)
    db.commit()

    return {new_screen}



def create_show_item(db:Session,item:CreateShowItem):
    
    new_item=ShowItem(
        show_id=item.show_id,
        quantity=item.quantity,
        seats=item.quantity
        
    )
    db.add(new_item)
    db.commit()

    return {new_item}

def create_seats(db:Session,seat:CreateSeat):
    new_seat=db.query(Seat).filter(Seat.show_id==seat.show_id).first()

    if new_seat:
        raise HTTPException(status_code=400,detail="seats exist for given show")
    new_seat=Seat(
        available_seats=seat.available_seats,
        booked_seats=seat.booked_seats,
        price=seat.price,
        screen_id=seat.screen_id,
        show_id=seat.show_id

    )
    db.add(new_seat)
    db.commit()

    return {"available_seats":new_seat.available_seats,"screen_id":new_seat.screen_id,"show_id":new_seat.show_id}

def create_show(db:Session,show:CreateShow):
    new_show=db.query(Show).filter(Show.screen_id==show.screen_id,
                                   Show.movie_name==show.movie_name,
                                   Show.end_time>show.start_time,
                                   
                                   ).first()
    
    if new_show:
        raise HTTPException(detail="this show exists")
    new_show=Show(
        screen_id=show.screen_id,
        movie_name=show.movie_name,
        start_time=show.start_time,
        end_time=show.end_time,
        
    )

    db.add(new_show)
    db.commit()

    return {new_show}

def get_all_screens(db:Session):
    screens=db.query(Screen).all()
    if not screens:
        raise HTTPException(status_code=404,detail="no screens found")
    return screens

def get_screen_seats(db:Session,Number:int):
    seats=db.query(Seat).filter(Seat.screen_id==Number).first()

   
    if not seats:
        raise HTTPException(status_code=400,detail="seats not found")
  
    return seats



def get_screen_shows(db:Session,Number:int):
    shows=db.query(Show).filter(Show.screen_id==Number).first()

    if not shows:
        raise HTTPException(status_code=400,detail="screen not found")
    
    
    return shows


def get_all_shows(db:Session):
    shows=db.query(Show).all()

    if not shows:
        raise HTTPException(status_code=400,detail="no shows found")
    return shows