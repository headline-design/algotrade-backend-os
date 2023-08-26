from __future__ import annotations
from sqlalchemy.orm import Session
from typing import Optional
from app.models.pool_assets import PAssets
from app.models.tx_pool import TxPool
from app.models.assets import Asset_s
from sqlalchemy.sql.expression import text


def get_count(
    db: Session,
    skip: int = 0,
    page_num: int = 1,
    page_size: int = 10,
    limit: Optional[int] = None,
):
    return (
        db.query(TxPool.pool_id)
        .join(PAssets, PAssets.pool_id == TxPool.pool_id)
        .join(Asset_s, Asset_s.id == PAssets.asset_1_id)
        .filter(PAssets.asset_2_id == "0")
        .filter(PAssets.pool == "TMPOOL11")
        .filter(TxPool.timestamp > text("NOW() - INTERVAL '1 DAY'"))
        # .filter(Asset_s.is_verified == "true")
        .filter(PAssets.pool_id != 552647097)
        .filter(PAssets.pool_id != 552666290)
        .filter(PAssets.pool_id != 552705765)
        .filter(PAssets.pool_id != 552921263)
        .filter(PAssets.pool_id != 552719953)
        .filter(PAssets.pool_id != 552722020)
        .filter(PAssets.pool_id != 552679552)
        .filter(PAssets.pool_id != 694683000)
        .filter(PAssets.pool_id != 685791182)
        .group_by(TxPool.pool_id, PAssets.pool_id, Asset_s.id)
        # .having(text("last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) > 100"))
        .offset(skip)
        .limit(limit)
        .count()
    )

def get_count_1(
    db: Session,
    skip: int = 0,
    page_num: int = 1,
    page_size: int = 10,
    limit: Optional[int] = None,
):
    return (
        db.query(TxPool.pool_id)
        .join(PAssets, PAssets.pool_id == TxPool.pool_id)
        .join(Asset_s, Asset_s.id == PAssets.asset_1_id)
        .filter(PAssets.asset_2_id == "0")
        .filter(PAssets.pool == "TMPOOL11")
        .filter(TxPool.timestamp > text("NOW() - INTERVAL '1 DAY'"))
        .filter(Asset_s.is_verified == "true")
        .filter(PAssets.pool_id != 552647097)
        .filter(PAssets.pool_id != 552666290)
        .filter(PAssets.pool_id != 552705765)
        .filter(PAssets.pool_id != 552921263)
        .filter(PAssets.pool_id != 552719953)
        .filter(PAssets.pool_id != 552722020)
        .filter(PAssets.pool_id != 552679552)
        .filter(PAssets.pool_id != 694683000)
        .filter(PAssets.pool_id != 685791182)
        .group_by(TxPool.pool_id, PAssets.pool_id, Asset_s.id)
        # .having(text("last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) > 100"))
        .offset(skip)
        .limit(limit)
        .count()
    )
def get_count_2(
    db: Session,
    skip: int = 0,
    page_num: int = 1,
    page_size: int = 10,
    limit: Optional[int] = None,
):
    return (
        db.query(TxPool.pool_id)
        .join(PAssets, PAssets.pool_id == TxPool.pool_id)
        .join(Asset_s, Asset_s.id == PAssets.asset_1_id)
        .filter(PAssets.asset_2_id == "0")
        .filter(PAssets.pool == "TMPOOL11")
        .filter(TxPool.timestamp > text("NOW() - INTERVAL '1 DAY'"))
        # .filter(Asset_s.is_verified == "true")
        .filter(PAssets.pool_id != 552647097)
        .filter(PAssets.pool_id != 552666290)
        .filter(PAssets.pool_id != 552705765)
        .filter(PAssets.pool_id != 552921263)
        .filter(PAssets.pool_id != 552719953)
        .filter(PAssets.pool_id != 552722020)
        .filter(PAssets.pool_id != 552679552)
        .filter(PAssets.pool_id != 694683000)
        .filter(PAssets.pool_id != 685791182)
        .group_by(TxPool.pool_id, PAssets.pool_id, Asset_s.id)
        .having(text("last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) > 100"))
        .offset(skip)
        .limit(limit)
        .count()
    )

def get_count_3(
    db: Session,
    skip: int = 0,
    page_num: int = 1,
    page_size: int = 10,
    limit: Optional[int] = None,
):
    return (
        db.query(TxPool.pool_id)
        .join(PAssets, PAssets.pool_id == TxPool.pool_id)
        .join(Asset_s, Asset_s.id == PAssets.asset_1_id)
        .filter(PAssets.asset_2_id == "0")
        .filter(PAssets.pool == "TMPOOL11")
        .filter(TxPool.timestamp > text("NOW() - INTERVAL '1 DAY'"))
        .filter(Asset_s.is_verified == "true")
        .filter(PAssets.pool_id != 552647097)
        .filter(PAssets.pool_id != 552666290)
        .filter(PAssets.pool_id != 552705765)
        .filter(PAssets.pool_id != 552921263)
        .filter(PAssets.pool_id != 552719953)
        .filter(PAssets.pool_id != 552722020)
        .filter(PAssets.pool_id != 552679552)
        .filter(PAssets.pool_id != 694683000)
        .filter(PAssets.pool_id != 685791182)
        .group_by(TxPool.pool_id, PAssets.pool_id, Asset_s.id)
        .having(text("last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) > 100"))
        .offset(skip)
        .limit(limit)
        .count()
    )

def get_favorite_pool(
    pool_id: Optional[int] = None
):
    return f"""
            SELECT 
            a.asset_1_id,
            c.name as asa_name,
            a.asset_1_name as unit_name,
            a.asset_1_decimals,
            c.is_verified,
            s.pool_id,
            LAST(liquidity_2/liquidity_1, timestamp) AS current_price,
            CASE WHEN
                z.hourly IS NULL THEN 0
            ELSE z.hourly
            END AS "1h_change",            
            (LAST(liquidity_2/liquidity_1, timestamp) - FIRST(liquidity_2/liquidity_1, timestamp)) / FIRST(liquidity_2/liquidity_1, timestamp) * 100 AS "1d_change",                                
            LAST(c.circulating_supply*liquidity_2/liquidity_1, timestamp) as market_cap,
            sum(amount_2) as volume,
            last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) as liquidity
            FROM tx_pool s
            LEFT JOIN HOUR z ON z.pool_id = s.pool_id				
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
            WHERE timestamp > NOW() - INTERVAL '1 day' and a.pool = 'TMPOOL11' and a.asset_2_id = 0 and not amount_2 < 0 and a.asset_1_id IN ({pool_id})
            GROUP BY s.pool_id , a.pool_id, a.asset_1_id, c.is_verified, c.name, z.hourly
            ORDER BY "asset_1_id" ASC
            LIMIT 10
	        """    


def get_pairs(
    sort_by: Optional[str] = None,
    offset: Optional[int] = None,
    order: Optional[str] = None,
):
    return f"""
            SELECT 
            a.asset_1_id,
            c.name as asa_name,
            a.asset_1_name as unit_name,
            a.asset_1_decimals,
            c.is_verified,
            s.pool_id,
            LAST(liquidity_2/liquidity_1, timestamp) AS current_price,
            CASE WHEN
                z.hourly IS NULL THEN 0
            ELSE z.hourly
            END AS "1h_change",            
            (LAST(liquidity_2/liquidity_1, timestamp) - FIRST(liquidity_2/liquidity_1, timestamp)) / FIRST(liquidity_2/liquidity_1, timestamp) * 100 AS "1d_change",                                
            LAST(c.circulating_supply*liquidity_2/liquidity_1, timestamp) as market_cap,
            sum(amount_2) as volume,
            last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) as liquidity
            FROM tx_pool s
            LEFT JOIN HOUR z ON z.pool_id = s.pool_id				
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
            WHERE timestamp > NOW() - INTERVAL '1 day' and a.pool = 'TMPOOL11' and a.asset_2_id = 0 and not amount_2 < 0 
            GROUP BY s.pool_id , a.pool_id, a.asset_1_id, c.is_verified, c.name, z.hourly
            ORDER BY "{sort_by}" {order} 
            LIMIT 10 offset {offset}
	        """
    

def get_pairs_1(
    sort_by: Optional[str] = None,
    offset: Optional[int] = None,
    order: Optional[str] = None,
):
    return f"""
            SELECT 
            a.asset_1_id,
            c.name as asa_name,
            a.asset_1_name as unit_name,
            a.asset_1_decimals,
            c.is_verified,
            s.pool_id,
            LAST(liquidity_2/liquidity_1, timestamp) AS current_price,
            CASE WHEN
                z.hourly IS NULL THEN 0
            ELSE z.hourly
            END AS "1h_change",            
            (LAST(liquidity_2/liquidity_1, timestamp) - FIRST(liquidity_2/liquidity_1, timestamp)) / FIRST(liquidity_2/liquidity_1, timestamp) * 100 AS "1d_change",                                
            LAST(c.circulating_supply*liquidity_2/liquidity_1, timestamp) as market_cap,
            sum(amount_2) as volume,
            last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) as liquidity
            FROM tx_pool s
            LEFT JOIN HOUR z ON z.pool_id = s.pool_id
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
            WHERE timestamp > NOW() - INTERVAL '1 day' and a.pool = 'TMPOOL11' and a.asset_2_id = 0 and not amount_2 < 0 and c.is_verified = 'true'
            GROUP BY s.pool_id , a.pool_id, a.asset_1_id, c.is_verified, c.name, z.hourly
            ORDER BY "{sort_by}" {order} 
            LIMIT 10 offset {offset}
	        """
    

def get_pairs_2(
    sort_by: Optional[str] = None,
    offset: Optional[int] = None,
    order: Optional[str] = None,
):
    return f"""
            SELECT 
            a.asset_1_id,
            c.name as asa_name,
            a.asset_1_name as unit_name,
            a.asset_1_decimals,
            c.is_verified,
            s.pool_id,
            LAST(liquidity_2/liquidity_1, timestamp) AS current_price,
            CASE WHEN
                z.hourly IS NULL THEN 0
            ELSE z.hourly
            END AS "1h_change",            
            (LAST(liquidity_2/liquidity_1, timestamp) - FIRST(liquidity_2/liquidity_1, timestamp)) / FIRST(liquidity_2/liquidity_1, timestamp) * 100 AS "1d_change",                                
            LAST(c.circulating_supply*liquidity_2/liquidity_1, timestamp) as market_cap,
            sum(amount_2) as volume,
            last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) as liquidity
            FROM tx_pool s
            LEFT JOIN HOUR z ON z.pool_id = s.pool_id				
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
            WHERE timestamp > NOW() - INTERVAL '1 day' and a.pool = 'TMPOOL11' and a.asset_2_id = 0 and not amount_2 < 0
            GROUP BY s.pool_id , a.pool_id, a.asset_1_id, c.is_verified, c.name, z.hourly
            having last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) > 100                
            ORDER BY "{sort_by}" {order} 
            LIMIT 10 offset {offset}
	        """

def get_pairs_3(
    sort_by: Optional[str] = None,
    offset: Optional[int] = None,
    order: Optional[str] = None,
):
    return f"""
            SELECT 
            a.asset_1_id,
            c.name as asa_name,
            a.asset_1_name as unit_name,
            a.asset_1_decimals,
            c.is_verified,
            s.pool_id,
            LAST(liquidity_2/liquidity_1, timestamp) AS current_price,
            CASE WHEN
                z.hourly IS NULL THEN 0
            ELSE z.hourly
            END AS "1h_change",            
            (LAST(liquidity_2/liquidity_1, timestamp) - FIRST(liquidity_2/liquidity_1, timestamp)) / FIRST(liquidity_2/liquidity_1, timestamp) * 100 AS "1d_change",                                
            LAST(c.circulating_supply*liquidity_2/liquidity_1, timestamp) as market_cap,
            sum(amount_2) as volume,
            last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) as liquidity
            FROM tx_pool s
            LEFT JOIN HOUR z ON z.pool_id = s.pool_id				
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
            WHERE timestamp > NOW() - INTERVAL '1 day' and a.pool = 'TMPOOL11' and a.asset_2_id = 0 and not amount_2 < 0 and c.is_verified = 'true'
            GROUP BY s.pool_id , a.pool_id, a.asset_1_id, c.is_verified, c.name, z.hourly
            having last(liquidity_1 * liquidity_2/liquidity_1 + liquidity_2, timestamp) > 100                
            ORDER BY "{sort_by}" {order} 
            LIMIT 10 offset {offset}
	        """

def with_select_as(
    db: Session,
    main_statement: Optional[str] = None,
):
    return db.execute(
        f"""
            with hour as(
                SELECT 
				pool_id,
                case when
					(LAST(liquidity_2/liquidity_1, timestamp) - FIRST(liquidity_2/liquidity_1, timestamp)) / FIRST(liquidity_2/liquidity_1, timestamp) * 100 is null then 0.00
				else
					(LAST(liquidity_2/liquidity_1, timestamp) - FIRST(liquidity_2/liquidity_1, timestamp)) / FIRST(liquidity_2/liquidity_1, timestamp) * 100		
				end AS hourly
                FROM tx_pool where timestamp > NOW() - INTERVAL '1 hour' group by pool_id
            )        
            {main_statement}
	    """
    )        