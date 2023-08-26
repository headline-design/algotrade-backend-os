from __future__ import annotations
from sqlalchemy.orm import Session
from app.models.pool_assets import PAssets
from app.models.assets import Asset_s


def get_asa_deets(db: Session, a1id: int):
    return (
        db.query(
            PAssets.pool_id,
            PAssets.asset_1_id,
            Asset_s.name,
            PAssets.asset_1_name,
            PAssets.asset_1_decimals,
            PAssets.asset_2_id,
            PAssets.asset_2_name,
            PAssets.asset_2_decimals,
            Asset_s.is_verified,
            Asset_s.url,
            PAssets.pool_creator,
            Asset_s.creator,
            Asset_s.reserve,
            Asset_s.total_amount,
            Asset_s.circulating_supply,
        )
        .join(Asset_s, Asset_s.id == PAssets.asset_1_id)
        .filter(PAssets.asset_1_id == a1id)
        .filter(PAssets.asset_2_id == "0")
        .filter(PAssets.pool == "TMPOOL11")
        .all()
    )

def getAsaId(db: Session, a1id: int):
    return (
        db.query(
            PAssets.pool_id,
            PAssets.asset_1_id
        )
        .join(Asset_s, Asset_s.id == PAssets.asset_1_id)
        .filter(PAssets.asset_1_id == a1id)
        .filter(PAssets.asset_2_id == 0)
        .filter(PAssets.pool == "TMPOOL11")
        .all()
    )

def post_asa(db: Session, a1id: int, algo_id: int):
    return db.execute(
        f"""
            WITH buckets AS (
            SELECT
            LAST(liquidity_2/liquidity_1, timestamp) AS current_price
            FROM tx_pool s
            INNER JOIN pool_assets a ON (a.pool_id = s.pool_id)
            WHERE timestamp > NOW() - INTERVAL '1 day' and a.asset_1_id = {algo_id} and a.asset_2_id = 0 and a.pool = 'TMPOOL11'
            ),
            bucketss AS (
            SELECT 
            LAST(c.circulating_supply*(s.liquidity_2/s.liquidity_1), s.timestamp) as market_cap,
            sum(s.amount_2) as volume,
            last(s.liquidity_1 * s.liquidity_2/s.liquidity_1 + s.liquidity_2, s.timestamp) AS liquidity
            FROM tx_pool s
            INNER JOIN pool_assets a ON (a.pool_id = s.pool_id)
            INNER JOIN assets c ON c.id = a.asset_1_id 
            WHERE s.timestamp > NOW() - INTERVAL '1 day' and a.pool_id = {a1id}
            and not s.amount_2 < 0
            GROUP BY s.pool_id , a.pool_id, a.asset_1_id, c.is_verified, c.name 
            )
            SELECT * FROM buckets, bucketss      
        """
    )


def get_asa(db: Session, a1id: int):
    return db.execute(
        f"""
                SELECT 
                LAST(liquidity_2/liquidity_1, timestamp) AS current_price,
                LAST(c.circulating_supply*(liquidity_2/liquidity_1), timestamp) as market_cap,
                sum(amount_2) as volume,
                last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) AS liquidity
                FROM tx_pool s
                INNER JOIN pool_assets a ON (a.pool_id = s.pool_id)
                INNER JOIN assets c ON c.id = a.asset_1_id 
                WHERE timestamp > NOW() - INTERVAL '1 day' and a.pool_id = {a1id}
                GROUP BY s.pool_id , a.pool_id, a.asset_1_id, c.is_verified, c.name
 
    """
    )


def get_rank(db: Session):
    return db.execute(
        """    				
                WITH one_day AS (
                    SELECT 
                    s.pool_id,
                    last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) as liquidity
                    FROM tx_pool s
                    INNER JOIN pool_assets a ON (a.pool_id = s.pool_id
                        and not a.pool_id = 552647097
                        and not a.pool_id = 552666290
                        and not a.pool_id = 552679552
                        and not a.pool_id = 552722020
                        and not a.pool_id = 552719953
                        and not a.pool_id = 552921263
                        and not a.pool_id = 552705765
                        and not a.pool_id = 694683000
                        and not a.pool_id = 685791182
                        )
                    INNER JOIN assets c ON c.id = a.asset_1_id 
                    WHERE timestamp > NOW() - INTERVAL '1 day' and a.asset_2_id = 0
                    GROUP BY s.pool_id
                    order by liquidity desc
                    )
                    SELECT
                    one_day.pool_id,
                    rank() over (order by one_day.liquidity desc) 
                    FROM one_day
                    INNER JOIN pool_assets c ON (c.pool_id = one_day.pool_id
                        and not c.pool_id = 552647097
                        and not c.pool_id = 552666290
                        and not c.pool_id = 552679552
                        and not c.pool_id = 552722020
                        and not c.pool_id = 552719953
                        and not c.pool_id = 552921263
                        and not c.pool_id = 552705765
                        and not c.pool_id = 694683000
                        and not c.pool_id = 685791182                        
                        )
                        INNER JOIN assets e on e.id = c.asset_1_id
                    GROUP BY one_day.pool_id, one_day.liquidity
                    order by one_day.liquidity desc
    """
    )


def get_asa_pairs(db: Session, a1id: int):
    return db.execute(
        f"""
            SELECT
            a.id,
            a.unit_name,
            s.asset_2_id,
            s.asset_2_name,
            s.pool_id,
            s.pool_creator,
			CASE WHEN 
				ss.pool_creator is NULL
			THEN s.pool_creator
			ELSE
				ss.pool_creator
			END AS algo_pool,
            s.asset_2_decimals        
            FROM pool_assets s
            LEFT JOIN pool_assets ss ON (ss.asset_1_id = s.asset_2_id
										 and ss.asset_2_id = 0)			
            INNER JOIN assets a ON (a.id = s.asset_1_id)
            INNER JOIN tx_pool aa ON (aa.pool_id = s.pool_id)		
            WHERE 
            timestamp > NOW() - INTERVAL '1 day' and
            s.asset_1_id = {a1id} AND s.pool = 'TMPOOL11'
            AND NOT s.asset_2_name = 'TMPOOL11'
            AND NOT s.asset_1_name = 'TMPOOL11'
            GROUP BY         
            a.id,
            a.unit_name,
            s.asset_2_id,
            s.asset_2_name,
            s.pool_id,
            s.pool_creator,
			ss.pool_creator,
            s.asset_2_decimals 
            ORDER BY s.asset_2_id ASC  
        """ 
    )
