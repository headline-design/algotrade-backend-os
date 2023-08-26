from sqlalchemy.orm import Session


def get_traded(db: Session):
    return db.execute('''
				SELECT 
				count(*) as total_trade,
				c.name,
				a.asset_1_id,
				a.asset_2_id,
				c.is_verified
				FROM tx_pool s
				INNER JOIN pool_assets a ON (a.pool_id = s.pool_id
											and not a.pool_id = 552647097
											and not a.pool_id = 552666290
											and not a.pool_id = 552679552
											and not a.pool_id = 552722020
											and not a.pool_id = 552719953
											and not a.pool_id = 552921263
											and not a.pool_id = 552705765)
				INNER JOIN assets c ON c.id = a.asset_1_id 
				WHERE timestamp > NOW() - INTERVAL '1 day' and a.asset_2_id = 0
				GROUP BY s.pool_id , a.pool_id, a.asset_1_id, c.url, c.unit_name, c.is_verified, c.name
				ORDER BY total_trade DESC 
				limit 3
			''')