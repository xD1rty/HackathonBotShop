from core.backend.db.db_setup import Base
from sqlalchemy import Column, BigInteger, String, Integer, Boolean
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    products = relationship('Product', back_populates='category')
