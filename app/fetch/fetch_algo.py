from sqlalchemy.orm import Session


def fetch_algorand(db: Session):
    return db.execute(
        f""" 

				
                SELECT time_bucket('1 hour', timestamp) AS bucket, 
                LAST(liquidity_1/liquidity_2, timestamp) AS close_price
                FROM tx_pool s
				INNER JOIN pool_assets a ON a.pool_id = s.pool_id				
                WHERE a.pool_id = 552647097	and timestamp > NOW() - INTERVAL '7 day'
                GROUP BY bucket, a.pool_id
                ORDER BY bucket
            """
    )


def fetch_latest(db: Session):
    return db.execute(
        f""" 
                SELECT time_bucket('1 day', timestamp) AS date,
				LAST(liquidity_1/liquidity_2, timestamp) AS close_price,
				(LAST(liquidity_1/liquidity_2, timestamp) - FIRST(liquidity_1/liquidity_2, timestamp)) / FIRST(liquidity_1/liquidity_2, timestamp) * 100 AS percentage_diff                         				
                FROM tx_pool s
				INNER JOIN pool_assets a ON a.pool_id = s.pool_id
                WHERE a.pool_id = 552647097	and timestamp > NOW() - INTERVAL '1 day'
                GROUP BY date, a.pool_id
                ORDER BY date
				

            """
    )
