
from collections import UserList
from sqlalchemy import CheckConstraint, Column,Integer, Nullable,String,JSON,ForeignKey,DateTime,ARRAY, column
from sqlalchemy.orm import relationship

from database import Base

class Screen(Base):
    __tablename__="screens"
    id=Column(Integer,nullable=False,primary_key=True,unique=True)
    number=Column(Integer,nullable=False,unique=True)
    seats=relationship("Seat",back_populates="screen")
    shows=relationship("Show",back_populates="screen")
    
    
    
class ShowItem(Base):
    __tablename__="show_items"
    id=Column(Integer,nullable=False,primary_key=True,unique=True)
    user_id=Column(ForeignKey("users.id"),nullable=False)
    seats=relationship("ShowItemSeat",back_populates="show_item")
    show=relationship("Show",back_populates="show_items",uselist=False)
    show_id=Column(Integer, ForeignKey("shows.id"), nullable=False)
 
    def total(self):
        return sum(item.seat.price for item in self.seats)

    


class ShowItemSeat(Base):
    __tablename__="show_item_seats"
    id=Column(Integer,nullable=False,primary_key=True,unique=True)
    show_item=relationship("ShowItem",back_populates="seats")
    seat=relationship("Seat")
    seat_id=Column(Integer,ForeignKey("seats.id"),nullable=False)
    show_item_id=Column(Integer,ForeignKey("show_items.id"),nullable=False)


class Seat(Base):
    __tablename__="seats"
    id=Column(Integer,nullable=False,primary_key=True,unique=True)
    seatname=Column(String)
    screen=relationship("Screen",back_populates="seats")
    price=Column(Integer)
    
    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)

class Show(Base):
    __tablename__="shows"
    id=Column(Integer,nullable=False,primary_key=True,unique=True)

    
    screen=relationship("Screen",back_populates="shows",uselist=False)
    show_items=relationship("ShowItem",back_populates="show")

    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)
    start_time=Column(DateTime)
    end_time=Column(DateTime)
    movie_name=Column(String)
    __table_args__=(
        CheckConstraint('end_time > start_time',name='end after start'),
    )
   


    