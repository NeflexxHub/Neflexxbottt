from sqlalchemy import (Column, Integer, BigInteger, String, DateTime, JSON, Text, Enum, create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    funpay_order_id = Column(String, unique=True, nullable=True)
    buyer_tg_id = Column(BigInteger, nullable=False)
    lot_id = Column(String, nullable=True)
    amount = Column(Integer, nullable=False, default=1)
    price = Column(Integer, nullable=False, default=0)
    status = Column(String, nullable=False, default='new')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # 'stars' or 'premium'
    amount = Column(Integer, nullable=False)
    provider_ref = Column(String, nullable=True)
    status = Column(String, nullable=False, default='available')  # available|reserved|used
    reserved_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class OrderEvent(Base):
    __tablename__ = 'order_events'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def get_engine(path='sqlite:///./funpay_cardinal.db'):
    return create_engine(path, connect_args={"check_same_thread": False})

def init_db(path='sqlite:///./funpay_cardinal.db'):
    engine = get_engine(path)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
