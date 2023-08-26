from __future__ import annotations
from sqlalchemy.orm import Session


def get_search(db: Session):
    return db.execute(f'''
                SELECT
                a.name,
                s.asset_1_name,
                a.id as asset_1_id,
                s.pool_id,
                a.is_verified,
                s.asset_1_decimals,
				s.pool_creator,
                case when a.reserve = a.creator then a.reserve
                else a.creator
                end as address
                FROM pool_assets s
                INNER JOIN assets a ON (a.id = s.asset_1_id)
                WHERE s.pool = 'TMPOOL11' and s.asset_2_id = 0
				order by asset_1_id asc, is_verified desc
    ''')
