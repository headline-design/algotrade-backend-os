from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_pools
from sqlalchemy.orm import Session
from app.api.token import verify_token
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/{a1id}")
def asa_list(
    a1id: int,
    db: Session = Depends(deps.get_db),
    authorized: bool = Depends(verify_token),
):
    try:
        asa = jsonable_encoder(fetch_pools.get_asa_deets(db, a1id))
        if bool(asa) is False or authorized is False:
            raise HTTPException(status_code=401, detail="Not found")    
        asa_pair = jsonable_encoder(list(fetch_pools.get_asa_pairs(db, a1id)))
        if asa_pair is None or authorized is False:
            raise HTTPException(status_code=401, detail="Not found")
        return list(asa_pair)
    except Exception:
        raise HTTPException(status_code=500, detail="Not found")
