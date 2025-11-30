
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from database import get_db
from methods.show_method import create_screen, create_seats, create_show_item, get_all_screens, get_screen_seats
from schemas import CreateScreen, CreateSeat, CreateShowItem
router=APIRouter()
@router.put("/screen")
def screen_create(screen:CreateScreen,db:Session=Depends(get_db)):
    return create_screen(db,screen)
@router.put("/show_item")
def show_item_create(item:CreateShowItem,db:Session=Depends(get_db)):
    return create_show_item(db,item)

@router.put("/seats")
def seats_create(seat:CreateSeat,db:Session=Depends(get_db)):
    return create_seats(db,seat)


@router.get("/screen")
def screen_display(db:Session=Depends(get_db)):
    return get_all_screens(db)    

@router.get("/seats")
def screen_seats_display(Number:int,db:Session=Depends(get_db)):
    return get_screen_seats(db,Number)
