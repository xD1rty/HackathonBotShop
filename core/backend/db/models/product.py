from core.backend.db.db_setup import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import ARRAY


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    price = Column(Integer)
    photos = Column(ARRAY(String))
