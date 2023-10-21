from core.backend.db.db_setup import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    message_type = Column(String)
    title = Column(String)
    description = Column(String)
    price = Column(Integer)
    photo = Column(String, default=None)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='products')
