from sqlalchemy.orm import Session
from app.models.tx_pool import TxPool
from typing import Optional


def get_account(db: Session, address: str):
    return db.query(TxPool.address).filter(TxPool.address == address).limit(1).all()


def tx_count(db: Session, address: str):
    return db.execute(
        f"""
            SELECT 
            count(*)
            FROM tx_pool s
            INNER JOIN pool_assets a ON a.pool_id = s.pool_id
            INNER JOIN assets aa ON aa.id = a.asset_1_id
            INNER JOIN assets aaa ON aaa.id = a.asset_2_id
            WHERE address = {address}
        """
    )


def get_volume(db: Session, address: str):
    return db.execute(
        f""" 
                SELECT 
				a.pool_id,				
                s.timestamp as date,
				aa.decimals as asset_1_decimals,
				aaa.decimals as asset_2_decimals,
                aa.id as asset_1_id,
                aaa.id as asset_2_id,
                aa.unit_name as asset_1_name,
                aaa.unit_name as asset_2_name,
				CASE WHEN s.asset_1_id = 'sell' 
					THEN 'sell'
				ELSE
					'buy'
				END AS type,
				s.group_id,
                s.amount_1,
                s.amount_2,
				round((s.liquidity_2/s.liquidity_1), 8) as total_price	
                FROM tx_pool s
                INNER JOIN pool_assets a ON a.pool_id = s.pool_id
				INNER JOIN assets aa ON aa.id = a.asset_1_id
				INNER JOIN assets aaa ON aaa.id = a.asset_2_id
                WHERE address = '{address}'
                ORDER BY date desc
				limit 5

    """
    )


def get_account_tx(
    db: Session,
    address: str,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int]= None,
    offset: Optional[int] = None,
):
    return db.execute(
        f"""             
                SELECT 
				a.pool_id,				
                s.timestamp as date,
				aa.decimals as asset_1_decimals,
				aaa.decimals as asset_2_decimals,
                aa.id as asset_1_id,
                aaa.id as asset_2_id,
                aa.unit_name as asset_1_name,
                aaa.unit_name as asset_2_name,
				CASE WHEN s.asset_1_id = 'sell' 
					THEN 'sell'
				ELSE
					'buy'
				END AS type,
				s.group_id,
                s.amount_1,
                s.amount_2,
				round((s.liquidity_2/s.liquidity_1), 8) as total_price	
                FROM tx_pool s
                INNER JOIN pool_assets a ON a.pool_id = s.pool_id
				INNER JOIN assets aa ON aa.id = a.asset_1_id
				INNER JOIN assets aaa ON aaa.id = a.asset_2_id
                WHERE address = {address}
                ORDER BY {sort_by} {order}
                limit {limit} OFFSET {offset}
            """
    )


def get_account_pool(db: Session, address: str):
    return db.execute(
        f"""             
                SELECT 
				a.pool_id,
				aa.id as asset_1_id,
                aa.unit_name as asset_1_name,
				aaa.id as asset_2_id,
                aaa.unit_name as asset_2_name
                FROM tx_pool s
                INNER JOIN pool_assets a ON a.pool_id = s.pool_id
				INNER JOIN assets aa ON aa.id = a.asset_1_id
				INNER JOIN assets aaa ON aaa.id = a.asset_2_id
                WHERE address = '{address}'
				group by a.pool_id, aa.unit_name, aaa.unit_name, aa.id, aaa.id
                ORDER BY a.pool_id asc
            """
    )
