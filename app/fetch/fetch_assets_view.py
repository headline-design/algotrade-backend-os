from __future__ import annotations
from sqlalchemy.orm import Session
from typing import Optional
from app.models.pool_assets import PAssets
from app.models.assets import Asset_s

def get_current_view(asset: int):
    return f"""
        with new_count as(
        select sum
        (
            case when type = '
            leave
            ' then 0 else count end
        ) as new_count
        from assets_view where id = {asset} and type ='new'
        ), leave_count as(
        select sum
        (
            case when type = '
            leave
            ' then 0 else count end
        ) as leave_count
        from assets_view where id = {asset} and type ='leave'
        )
        select
        new_count.new_count-
        case when leave_count.leave_count is null
            then 0
        else
            leave_count.leave_count
        end
        as current_view
        from new_count, leave_count
    """

def insert_view(db: Session, asset: int, date: str, reason: str):
    db.execute(
        f"""
            INSERT INTO assets_view
            (id, timestamp, count, type)
            VALUES ({asset}, '{date}+00', 1, '{reason}')
        """
    )
    db.commit()
    return db.execute(
        get_current_view(asset)
    )