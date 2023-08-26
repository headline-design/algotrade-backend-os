from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_pools, fetch_live
from sqlalchemy.orm import Session
from app.api.token import verify_token
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/{a1id}")
def post_assets(
    a1id: int,
    db: Session = Depends(deps.get_db),
    authorized: bool = Depends(verify_token),
):
    try:
        asa = jsonable_encoder(fetch_live.get_pool_id(db, a1id))
        if bool(asa) is False or authorized is False:
            raise HTTPException(status_code=401, detail="Not found")   
        algo_price = jsonable_encoder(fetch_live.get_pool_idd(db, a1id))
        asa_pair = jsonable_encoder(list(fetch_pools.post_asa(db, a1id, jsonable_encoder(algo_price[0]["asset_2_id"]))))
        if asa_pair is None or authorized is False:
            raise HTTPException(status_code=401, detail="Not found")
        return list(asa_pair)
    except Exception:
        raise HTTPException(status_code=500, detail="Not found")
