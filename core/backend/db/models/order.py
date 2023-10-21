from core.backend.db.db_setup import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    status = Column(String, default=None)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')
