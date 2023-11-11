from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP,nullable=False,server_default=text('now()'))

class Bus(Base):
    __tablename__='bus'
    bus_id=Column(Integer,primary_key=True)
    bus_name=Column(String,unique=True)
    owner_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE',onupdate='CASCADE'))
    


class Stop(Base):
    __tablename__='stops'
    stop_id=Column(Integer,primary_key=True)
    created_user_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE',onupdate='CASCADE'))
    stop_name=Column(String,nullable=False,unique=True)
    is_active=Column(Boolean,default=True)
    created_at=Column(TIMESTAMP,nullable=False,server_default=text('now()'))