from core.backend.db.db_setup import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class ProductLottery(Base):
    __tablename__ = 'product_lotteries'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    balance = Column(Integer, default=0)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product')
    users = relationship('User')


class MoneyLottery(Base):
    __tablename__ = 'money_lotteries'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    balance = Column(Integer, default=0)
    money_prize = Column(Integer)
    users = relationship('User')
