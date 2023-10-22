from core.backend.db.db_setup import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship


product_lotteries_association = Table(
    "product_lotteries_association",
    Base.metadata,
    Column("product_lottery_id", ForeignKey("product_lotteries.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


money_lotteries_association = Table(
    "money_lotteries_association",
    Base.metadata,
    Column("money_lottery_id", ForeignKey("money_lotteries.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class ProductLottery(Base):
    __tablename__ = 'product_lotteries'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    balance = Column(Integer, default=0)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product')
    users = relationship('User', secondary=product_lotteries_association)


class MoneyLottery(Base):
    __tablename__ = 'money_lotteries'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    balance = Column(Integer, default=0)
    money_prize = Column(Integer)
    users = relationship('User', secondary=money_lotteries_association)
