from sqlalchemy.orm import Session

def fetch_algorand(db: Session):
    return db.execute(
        """
            WITH ok as (
                SELECT 
                count(*),
                sum(amount_2) as volume
                FROM tx_pool s
                INNER JOIN pool_assets a ON (a.pool_id = s.pool_id)
                INNER JOIN assets c ON c.id = a.asset_1_id 
                WHERE timestamp > NOW() - INTERVAL '1 day' and a.pool = 'TMPOOL11' and a.asset_2_id = 0
                LIMIT 10 offset 0
            ),
            okk as(
            SELECT count(*) as assets
            FROM assets where not unit_name = 'TMPOOL11'
            ),
            okkk as (
            SELECT count(*) as pool
            FROM pool_assets
            WHERE pool = 'TMPOOL11'
            )
            select * from ok, okk, okkk;
        """
    )
