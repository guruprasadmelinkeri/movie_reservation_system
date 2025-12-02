
from ctypes.wintypes import SHORT
import datetime
import json
from fastapi import HTTPException
from models.screen_models import Screen,Seat,ShowItem,Show, ShowItemSeat
from sqlalchemy.orm import Session

from schemas import CreateScreen, CreateSeat, CreateShow, CreateShowItem, CreateShowItemSeat


def create_screen(db:Session,screen:CreateScreen):
    new_screen=db.query(Screen).filter(Screen.number==screen.Number).first()
    if new_screen:
        raise HTTPException(status_code=400,detail="screen number taken")
    new_screen=Screen(
        number=screen.Number
        
    )
    db.add(new_screen)
    db.commit()

    return {new_screen}




def get_booked_seats(db:Session,show_id:int):
    seats = db.query(ShowItemSeat.seat_id).join(ShowItem).filter(ShowItem.show_id==show_id).all()
    return [s[0] for s in seats]

def seat_exists(db:Session,show_id:int,seat_id):
    screen_id=db.query(Show.screen_id).join(ShowItem).filter(ShowItem.show_id==show_id).scalar()
    screen=db.query(Screen).filter(Screen.id==screen_id).first()
    if not screen:
        return False
    seat=screen.seats

    seat=[s.id for s in seat]
    
    return seat_id in seat


def create_show_item(db:Session,item:CreateShowItem):
    
    new_item=ShowItem(
        show_id=item.show_id,
        user_id=item.user_id
    )
    db.add(new_item)
    db.commit()

    return {"total":new_item.total()}

def create_show_item_seat(db:Session,item:CreateShowItemSeat):
    show_item=db.query(ShowItem).filter(ShowItem.id==item.show_item_id).first()
    if not show_item:
        raise HTTPException(status_code=404, detail="show_item not found")
    show=db.query(Show).filter(Show.id==show_item.show_id).first()
    
    if get_booked_seats(db,item.seat_id):
        raise HTTPException(status_code=404, detail="seats is booked")
    if  not seat_exists(db,show.id,item.seat_id):
        raise HTTPException(status_code=404, detail="seat doesnt exist ")
    if datetime.datetime.now()>show.start_time:
        raise HTTPException(status_code=404,detail="show has started")
    
    show_item_seat=ShowItemSeat(
        seat_id=item.seat_id,
        show_item_id=item.show_item_id,
    )

    db.add(show_item_seat)
    db.commit()

    return {show_item.total()}
    
      


def create_seats(db:Session,seat:CreateSeat):
    new_seat=db.query(Seat).filter(Seat.screen_id==seat.screen_id,
                                   Seat.seatname==seat.seat_name).first()

    if new_seat:
        raise HTTPException(status_code=400,detail="seats exist for given show")
    new_seat=Seat(
       
        price=seat.price,
        screen_id=seat.screen_id,
        seatname=seat.seat_name
    )
    db.add(new_seat)
    db.commit()

    return {"screen_id":new_seat.screen_id,}

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
    seats=db.query(Seat).filter(Seat.screen_id==Number).all()

   
    if not seats:
        raise HTTPException(status_code=400,detail="seats not found")
  
    return [s for s in seats]



def get_screen_shows(db:Session,screen_id:int):
    screen=db.query(Screen).filter(Screen.id==screen_id).first()

    if not screen:
        raise HTTPException(status_code=400,detail="show not found")
    
    
    return screen.shows


def get_all_shows(db:Session):
    shows=db.query(Show).all()

    if not shows:
        raise HTTPException(status_code=400,detail="no shows found")
    return shows