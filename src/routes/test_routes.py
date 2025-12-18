
from fastapi import APIRouter,Depends
from fastapi import Request
from sqlalchemy.orm import Session

from auth.rbac import require
from database import get_db
from methods.show_method import create_screen, create_seats, create_show, create_show_item, create_show_item_seat, get_all_screens, get_all_shows, get_screen_seats, get_screen_shows, ticket_cancel
from methods.user_method import get_user
from schemas import CreateScreen, CreateSeat, CreateShow, CreateShowItem, CreateShowItemSeat, TicketCancel
router=APIRouter()

@router.put("/screen")
def screen_create(screen:CreateScreen,request:Request,db:Session=Depends(get_db)):
    user=get_user(db,request)
    require(user,"admin","super")
    return create_screen(db,screen)
@router.put("/show_item")
def show_item_create(item:CreateShowItem,request:Request,db:Session=Depends(get_db)):
    user=get_user(db,request)
    return create_show_item(db,user,item)

@router.put("/show_item/seat")
def show_item_seat_create(item:CreateShowItemSeat,request:Request,db:Session=Depends(get_db)):
    user=get_user(db,request)
    return create_show_item_seat(db,item)


@router.put("/seats")
def seats_create(seat:CreateSeat,request:Request,db:Session=Depends(get_db)):
    user=get_user(db,request)
    require(user,"admin","super")
    return create_seats(db,seat)

@router.put("/show")
def shows_create(show:CreateShow,request:Request,db:Session=Depends(get_db)):
    user=get_user(db,request)
    require(user,"admin","super")
    return create_show(db,show)



@router.get("/screen")
def screen_display(db:Session=Depends(get_db)):
    return get_all_screens(db)    

@router.get("/seats/screeen")
def screen_seats_display(Number:int,db:Session=Depends(get_db)):
    return get_screen_seats(db,Number)
@router.get("/shows/screen")
def screen_shows_display(Number:int,db:Session=Depends(get_db)):
    return get_screen_shows(db,Number)

@router.get("/shows")
def shows_all(db:Session=Depends(get_db)):
    return get_all_shows(db)
@router.delete("/show_item")

def cancel_ticket(item:TicketCancel,request:Request,db:Session=Depends(get_db)):
    user=get_user(db,request)
    require(user,"admin","super")
    return ticket_cancel(db,item)
