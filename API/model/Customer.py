from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from util.database import Base


class Customer(Base):
    __tablename__ = "Customer"
    customer_id = Column(Integer, primary_key=True)
    customerName = Column(String(100), unique=True)
    users = relationship("User", back_populates="customer")
    files = relationship("File", back_populates="customer")
