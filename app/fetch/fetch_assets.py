from __future__ import annotations
from sqlalchemy.orm import Session


def get_asset_id(db: Session):
    return db.execute(
        """
SELECT 
s.pool_id,
a.asset_1_id
FROM tx_pool s
INNER JOIN pool_assets a
    ON (a.pool_id = s.pool_id
    and not a.pool_id = 552647097
    and not a.pool_id = 552666290
    and not a.pool_id = 552679552
    and not a.pool_id = 552722020
    and not a.pool_id = 552719953
    and not a.pool_id = 552921263
    and not a.pool_id = 552705765)
WHERE timestamp > NOW() - INTERVAL '1 day'
and s.pool_id = a.pool_id
and a.pool = 'TMPOOL11'
and a.asset_2_id = 0
GROUP BY s.pool_id , a.pool_id
    """
    )
