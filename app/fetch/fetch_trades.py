from __future__ import annotations
from sqlalchemy.orm import Session
from typing import Optional
from app.models.pool_assets import PAssets


def get_pool_id(db: Session, pid: int):
    return db.query(PAssets.pool_id).filter(PAssets.pool_id == pid).filter(PAssets.pool == 'TMPOOL11').all()

def get_candle_count(db: Session, timeframe: Optional[str] = None, pool_id: Optional[int] = None):
    return db.execute(f'''
						WITH buckets AS (
							SELECT count(*) AS count_1
							FROM (						
							SELECT
							pool_id,
							time_bucket('{timeframe}', timestamp) AS datetime
							FROM tx_pool
							WHERE pool_id = {pool_id}
							GROUP BY datetime, pool_id
							ORDER BY datetime asc
							)s)
						select count_1 from buckets
						''')

def candleSticks(db: Session, limit: Optional[int] = None, timeframe: Optional[str] = None, pool_id: Optional[int] = None, offset: Optional[int] = None):
    return db.execute(f''' 
						SELECT
						time_bucket('{timeframe}', timestamp) AS datetime,
						CASE
						WHEN lag(last(total_price, timestamp)) over(order by time_bucket('{timeframe}', timestamp)) is NULL
							THEN FIRST(total_price, timestamp)
						ELSE lag(last(total_price, timestamp)) over(order by time_bucket('{timeframe}', timestamp))
						END as open,
						LAST(total_price, timestamp) AS close,
						MIN(total_price) AS low,
						MAX(total_price) AS high,
						SUM(amount_2_final) as volume
						FROM tx_pool
						WHERE pool_id = {pool_id}
						GROUP BY datetime, pool_id
						ORDER BY datetime asc
						LIMIT {limit} OFFSET {offset}
					''')	