from sqlalchemy.orm import Session

def fetch_latest(db: Session):
    return db.execute(
        f""" 
        SELECT time_bucket('1 day', timestamp) AS date,
        LAST(liquidity_2/liquidity_1, timestamp) AS close_price,
        (LAST(liquidity_2/liquidity_1, timestamp) - FIRST(liquidity_2/liquidity_1, timestamp)) / FIRST(liquidity_2/liquidity_1, timestamp) * 100 AS percentage_diff                         				
        FROM tx_pool s
        INNER JOIN pool_assets a ON a.pool_id = s.pool_id
        WHERE a.pool_id = 552706313	and timestamp > NOW() - INTERVAL '1 day'
        GROUP BY date, a.pool_id
        ORDER BY date		
        """
    )