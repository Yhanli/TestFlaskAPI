from fileinput import filename
from typing import Any
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from util.database import Base


class File(Base):
    __tablename__ = "File"
    file_id = Column(Integer, primary_key=True)
    path = Column(String(1000), unique=True)
    filename = Column(String(1000))

    customer_id = Column(Integer, ForeignKey("Customer"))
    customer = relationship("Customer")

    user_id = Column(Integer, ForeignKey("User"))
    user = relationship("User")
