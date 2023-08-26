from sqlalchemy.orm import Session


def get_volume(db: Session):
    return db.execute(f"""
        SELECT 
        a.asset_1_id,
        c.name as asa_name,
        a.asset_1_name as unit_name,
        a.asset_1_decimals,
        c.is_verified,
        LAST(liquidity_2/liquidity_1, timestamp) AS current_price,
        (LAST(liquidity_2/liquidity_1, timestamp) - FIRST(liquidity_2/liquidity_1, timestamp)) / FIRST(liquidity_2/liquidity_1, timestamp) * 100 AS percentage_diff                           
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
        WHERE timestamp > NOW() - INTERVAL '1 day' and a.pool = 'TMPOOL11' and a.asset_2_id = 0 and not amount_2 < 0
        GROUP BY s.pool_id , a.pool_id, a.asset_1_id, c.is_verified, c.name
		having last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) > 1000                		
        ORDER BY percentage_diff desc
        LIMIT 3 offset 0
    """)