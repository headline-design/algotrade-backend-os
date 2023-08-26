from sqlalchemy import Column, Integer, String
from app.db.session import Base
from sqlalchemy import *

class TxPool(Base):
    __tablename__ = "tx_pool"
    pool_id = Column(Integer, index=True)
    group_id = Column(String, primary_key=True)
    timestamp = Column(Date)
    address = Column(String)