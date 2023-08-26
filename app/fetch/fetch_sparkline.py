from typing import Optional
from sqlalchemy.orm import Session

def fetch_assets_sparkline(db: Session, pool_id: Optional[int] = None):
    return db.execute(
        f""" 
			select
			a.pool_id,
			bucket,
			close as close_price
			from candles_hourly aa
			INNER JOIN pool_assets a on aa.pool_id = a.pool_id
			WHERE a.pool_id = {pool_id} and aa.bucket > NOW() - INTERVAL '7 day'
			ORDER BY bucket asc
        """
    )