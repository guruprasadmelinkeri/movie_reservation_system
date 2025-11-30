
from ast import List
from sqlalchemy import Column,Integer,String,JSON,ForeignKey,DateTime
from sqlalchemy.orm import relationship

from database import Base

class Screen(Base):
    __tablename__="screens"
    id=Column(Integer,nullable=False,primary_key=True,unique=True)
    number=Column(Integer,nullable=False,unique=True)
    seats=relationship("Seat",back_populates="screen")
    seat_id=Column(Integer)
    
class ShowItem(Base):
    __tablename__="show_items"
    id=Column(Integer,nullable=False,primary_key=True,unique=True)
    seats=Column(JSON)
    screen_id=Column(Integer)
    quantity=Column(Integer)
    price=Column

    def total(self):
        return (self.price)*(self.quantity)

class Seat(Base):
    __tablename__="seats"
    id=Column(Integer,nullable=False,primary_key=True,unique=True)
    screen=relationship("Screen",back_populates="seats",uselist=False)
    
    available_seats=Column(JSON)
    price=Column(Integer)
    booked_seats=Column(JSON)
    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)



    