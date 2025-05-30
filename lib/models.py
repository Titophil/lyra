from sqlalchemy import Column, Integer, String,Float,ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime,timezone
from sqlalchemy.orm import declarative_base
import requests

from lib.db.database import engine

Base = declarative_base()

class Crypto(Base):
    __tablename__ = 'cryptos'

    id = Column(Integer, primary_key = True)
    symbol = Column(String, unique = True)
    name = Column(String)
    name_id = Column(String)
    rank = Column(Integer)
    price_usd = Column(Float)
    percent_change_24hrs = Column(Float)
    percent_change_1hrs = Column(Float)
    percent_change_7d  = Column(Float)
    price_btc = Column(Float)
    market_cap_usd = Column(Float)
    volume24 = Column(Float)
    volume24a = Column(Float)
    csupply = Column(Float)
    tsupply = Column(Float)
    msupply = Column(Float, nullable = True)

    holdings = relationship("Holding", back_populates="crypto", cascade="all, delete-orphan")

    def __repr__(self):
        return f"crypto {self.id}: " \
               + f"{self.name}: " \
               + f"{self.symbol}: " \
               + f" {self.price_usd}"


    
class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key = True)
        username = Column(String, unique = True)
        email = Column(String, unique = True)
        password = Column(String)
        balance_usd = Column(Float, default = 0.0)

        holdings = relationship("Holding", back_populates="user", cascade="all, delete-orphan")

class Holding(Base):
        __tablename__ = 'holdings'
        id = Column(Integer, primary_key = True)
        user_id = Column(Integer, ForeignKey("users.id"))
        crypto_id = Column(Integer, ForeignKey("cryptos.id"), nullable=False)
        crypto_symbol = Column(String)
        amount = Column(Float)


        user = relationship("User", back_populates="holdings")
        crypto = relationship("Crypto", back_populates="holdings")

class Transaction(Base):
        __tablename__ = 'transactions'
        id = Column(Integer, primary_key = True)
        user_id = Column(Integer, ForeignKey('users.id'))
        crypto_symbol = Column(String)
        amount = Column(Float)
        price_usd= Column(Float)
        type = Column(String)
        timestamp = Column(DateTime, default = lambda: datetime.now(timezone.utc))
    



