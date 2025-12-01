
from collections import UserList
from sqlalchemy import CheckConstraint, Column,Integer,String,JSON,ForeignKey,DateTime,ARRAY
from sqlalchemy.orm import relationship

from database import Base

class Screen(Base):
    __tablename__="screens"
    id=Column(Integer,nullable=False,primary_key=True,unique=True)
    number=Column(Integer,nullable=False,unique=True)
    seats=relationship("Seat",back_populates="screen")
    shows=relationship("Show",back_populates="screen")
    all_seats=Column(JSON)
    
    
class ShowItem(Base):
    __tablename__="show_items"
    id=Column(Integer,nullable=False,primary_key=True,unique=True)
    Screen_number=Column(Integer)
    seats=Column(JSON)
    show_id=Column(Integer, ForeignKey("shows.id"), nullable=False)
    quantity=Column(Integer)
    price=Column(Integer)
    

    def total(self):
        return (self.price)*(self.quantity)

class Seat(Base):
    __tablename__="seats"
    id=Column(Integer,nullable=False,primary_key=True,unique=True)
    screen=relationship("Screen",back_populates="seats")
    show=relationship("Show",back_populates="seat")
    show_id=Column(Integer, ForeignKey("shows.id"), nullable=False)
    available_seats=Column(JSON)
    price=Column(Integer)
    booked_seats=Column(JSON)
    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)

class Show(Base):
    __tablename__="shows"
    id=Column(Integer,nullable=False,primary_key=True,unique=True)
    seat=relationship("Seat",back_populates="show",uselist=False)
    screen=relationship("Screen",back_populates="shows")
    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)
    start_time=Column(DateTime)
    end_time=Column(DateTime)
    movie_name=Column(String)

    __table_args__=(
        CheckConstraint('end_time > start_time',name='end after start'),
    )
   


    