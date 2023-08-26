from __future__ import annotations
from sqlalchemy.orm import Session
from typing import Optional
from app.models.pool_assets import PAssets
from app.models.assets import Asset_s


def get_pool_id(db: Session, pid: int):
    return (
        db.query(PAssets.pool_id)
        .filter(PAssets.pool_id == pid)
        .filter(PAssets.pool == "TMPOOL11")
        .all()
    )
def get_asset_id(db: Session, pid: int):
    return (
        db.query(Asset_s.id)
        .filter(Asset_s.id == pid)
        .all()
    )
def get_asset_id_list(db: Session, pid):
    # result = db.query(Asset_s.id).filter(Asset_s.id == 27165954 27165954).all()
    # query = db.query(Asset_s.id).join(PAssets, PAssets.asset_1_id == Asset_s.id)
    # for value in pid:
    #     query = query.filter(PAssets.asset_1_id == value)
    # print(str(query))
    return (
        db.query(Asset_s.id, PAssets.pool_id)
        .join(Asset_s, Asset_s.id == PAssets.asset_1_id)
        .filter(Asset_s.id.in_(pid))
        .filter(PAssets.asset_2_id == 0)
        .all()        
    )        


def get_pool_idd(db: Session, pid: int):
    return (
        db.query(PAssets.asset_2_id)
        .join(Asset_s, Asset_s.id == PAssets.asset_2_id)
        .filter(PAssets.pool_id == pid)
        .filter(PAssets.pool == "TMPOOL11")
        .all()
    )

def tx_count(db: Session, pool_id: Optional[int] = None):
    return db.execute(
        f"""
            WITH buckets AS (
                SELECT count(*) AS count_1
                FROM (						
                SELECT
                pool_id,
                CASE WHEN amount_1 = 0.0
                    THEN 0
                ELSE				
                    amount_1
                END AS amount_1,
                CASE WHEN amount_2 = 0.0
                    THEN 0
                ELSE				
                    amount_2
                END AS amount_2
                FROM tx_pool
                WHERE pool_id = {pool_id} and not amount_1 <= 0 and not amount_2 <= 0
                )s)
            select count_1 from buckets
        """
    )
def tx_count_account(db: Session, pool_id: Optional[int] = None, address: Optional[str] = None):
    return db.execute(
        f"""
            WITH buckets AS (
                SELECT count(*) AS count_1
                FROM (						
                SELECT
                pool_id
                FROM tx_pool
                WHERE pool_id = {pool_id} and address = '{address}'
                )s)
            select count_1 from buckets
        """
    )

def percentage_tx(db: Session, pool_id: Optional[int] = None):
    return db.execute(
        f"""
            WITH hour as(
                SELECT 
                (LAST(liquidity_2/liquidity_1, timestamp) - FIRST(liquidity_2/liquidity_1, timestamp)) / FIRST(liquidity_2/liquidity_1, timestamp) * 100 AS hourly
                FROM tx_pool where timestamp > NOW() - INTERVAL '1 hour'
                and pool_id = {pool_id}
            ),
            daily as(
                SELECT
                (LAST(liquidity_2/liquidity_1, timestamp) - FIRST(liquidity_2/liquidity_1, timestamp)) / FIRST(liquidity_2/liquidity_1, timestamp) * 100 AS daily
                FROM tx_pool where timestamp > NOW() - INTERVAL '1 day'
                and pool_id = {pool_id}
            )
            SELECT * FROM hour, daily
        """
    )


def liveTx(
    db: Session,
    limit: Optional[int] = None,
    pool_id: Optional[int] = None,
    offset: Optional[int] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
):
    return db.execute(
        f""" 
            SELECT 
            a.pool_id,				
            s.timestamp as date,
            s.round,
            CASE WHEN s.asset_1_id = 'sell' 
                THEN 'sell'
            ELSE
                'buy'
            END AS type,
            s.group_id,
            s.address,
            CASE WHEN s.amount_1 = 0.0
                THEN 0
            ELSE				
                s.amount_1
            END AS amount_1,
            CASE WHEN s.amount_2 = 0.0
                THEN 0
            ELSE				
                s.amount_2
            END AS amount_2,
            round((s.liquidity_2/s.liquidity_1), 8) as total_price	
            FROM tx_pool s
            INNER JOIN pool_assets a ON a.pool_id = s.pool_id
            WHERE a.pool_id = {pool_id} and not s.amount_1 <= 0 and not s.amount_2 <= 0
            ORDER BY {sort_by} {order}
            limit {limit} OFFSET {offset}
        """
    )
def liveTxAccount(
    db: Session,
    limit: Optional[int] = None,
    pool_id: Optional[int] = None,
    offset: Optional[int] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    address: Optional[str] = None
):
    return db.execute(
        f""" 
            SELECT 
            a.pool_id,				
            s.timestamp as date,
            s.round,
            s.amount_1,
            s.amount_2,
            CASE WHEN s.asset_1_id = 'sell' 
                THEN 'sell'
            ELSE
                'buy'
            END AS type,            
            s.group_id,
            s.address,
            round((s.liquidity_2/s.liquidity_1), 8) as total_price	
            FROM tx_pool s
            INNER JOIN pool_assets a ON a.pool_id = s.pool_id
            WHERE a.pool_id = {pool_id} and s.address = '{address}'
            ORDER BY {sort_by} {order}
            limit {limit} OFFSET {offset}
        """
    )
