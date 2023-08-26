from sqlalchemy import Column, Integer, String
from app.db.session import Base

class PAssets(Base):
    __tablename__ = "pool_assets"
    pool_id = Column(Integer, primary_key=True, index=True)
    pool = Column(String)
    asset_1_id = Column(Integer)
    asset_1_name = Column(String)
    asset_1_decimals = Column(Integer)
    asset_2_id = Column(Integer)
    asset_2_name = Column(String)
    asset_2_decimals = Column(Integer)
    pool_creator = Column(String)

