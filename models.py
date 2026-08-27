from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="farmer")
