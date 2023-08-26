from typing import Optional
from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_sparkline, fetch_live
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.api.token import verify_token

router = APIRouter()


@router.get("/{pool_id}")
def get_assets_sparkline(
    pool_id: Optional[int] = None,
    db: Session = Depends(deps.get_db),
    authorized: bool = Depends(verify_token),
):
    try:
        pools = fetch_live.get_pool_id(db, pool_id)
        pid = jsonable_encoder(list(pools)[0]["pool_id"])
        if pid != pool_id:
            raise HTTPException(status_code=404, detail="Not found")
        else:        
            sparkline_query = fetch_sparkline.fetch_assets_sparkline(db, pid)
            response = {"response": jsonable_encoder(list(sparkline_query))}
            if sparkline_query is None or authorized is False:
                raise HTTPException(status_code=401, detail="Not found")
            return response
    except Exception:
        raise HTTPException(status_code=500, detail="Not found")
