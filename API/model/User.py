from typing import Any
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from util.database import Base


class User(Base):
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    customer_id = Column(Integer, ForeignKey("Customer"))
    customer = relationship("Customer")
    files = relationship("File", back_populates="user")
