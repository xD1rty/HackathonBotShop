from core.backend.db.db_setup import Base
from sqlalchemy import Column, BigInteger, String, Integer, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)  # в функциях ставим
    telegram_tag = Column(String)
    name = Column(String)
    position = Column(String)
    balance = Column(Integer, default=0)
    is_worker = Column(Boolean, default=None)
    tokens = relationship('Token', back_populates='user')
