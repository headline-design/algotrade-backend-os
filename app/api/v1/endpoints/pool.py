from typing import Optional
from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_pool
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.api.utils import paginationFast
from app.api.token import verify_token

router = APIRouter()


@router.get("")
def pool_asa(
    skip: int = 0,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    limit: int = 10,
    offset: Optional[int] = None,
    db: Session = Depends(deps.get_db),
    verified: Optional[str] = None,
    liquidity: Optional[str] = None,
    authorized: bool = Depends(verify_token),
):
    try:
        bool_filter = ["true", "false"]
        asc = [
            ("asa_name"),
            ("current_price"),
            ("1d_change"),
            ("1h_change"),
            ("volume"),
            ("market_cap"),
            ("liquidity"),
        ]
        desc = [("desc"), ("asc")]
        if (
            sort_by not in asc
            or order not in desc
            or verified not in bool_filter
            or liquidity not in bool_filter
            or authorized is False
        ):
            raise HTTPException(status_code=404, detail="Not found")
        else:
            if verified == "true" and liquidity == "false":
                count = jsonable_encoder(fetch_pool.get_count_1(db, skip=0))
                pools = fetch_pool.with_select_as(
                        db, fetch_pool.get_pairs_1(sort_by, offset, order)
                        )                      
                asa_pair = paginationFast(count, pools, offset, limit, sort_by, order)
                if pools is None or sort_by not in asc or order not in desc:
                    raise HTTPException(status_code=404, detail="Not found")
                return asa_pair
            if liquidity == "true" and verified == "false":
                count = jsonable_encoder(fetch_pool.get_count_2(db, skip=0))
                pools = fetch_pool.with_select_as(
                        db, fetch_pool.get_pairs_2(sort_by, offset, order)
                        )                      
                asa_pair = paginationFast(count, pools, offset, limit, sort_by, order)
                if pools is None or sort_by not in asc or order not in desc:
                    raise HTTPException(status_code=404, detail="Not found")
                return asa_pair
            if verified == "true" and liquidity == "true":
                count = jsonable_encoder(fetch_pool.get_count_3(db, skip=0))
                pools = fetch_pool.with_select_as(
                        db, fetch_pool.get_pairs_3(sort_by, offset, order)
                        )                
                asa_pair = paginationFast(count, pools, offset, limit, sort_by, order)
                if pools is None or sort_by not in asc or order not in desc:
                    raise HTTPException(status_code=404, detail="Not found")
                return asa_pair
            if verified == "false" and liquidity == "false":
                count = jsonable_encoder(fetch_pool.get_count(db, skip=0))
                pools = fetch_pool.with_select_as(
                        db, fetch_pool.get_pairs(sort_by, offset, order)
                        )
                asa_pair = paginationFast(count, pools, offset, limit, sort_by, order)
                if pools is None or sort_by not in asc or order not in desc:
                    raise HTTPException(status_code=404, detail="Not found")
                return asa_pair
    except Exception:
        raise HTTPException(status_code=500, detail="Not found")
