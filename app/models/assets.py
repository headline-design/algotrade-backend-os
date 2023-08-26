from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Asset_s(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    is_verified = Column(String)
    decimals = Column(Integer)
    creator = Column(String)
    reserve = Column(String)
    total_amount = Column(Integer)
    circulating_supply = Column(Integer)
