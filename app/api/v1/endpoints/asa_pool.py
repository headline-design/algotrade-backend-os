from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_pools
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.api.token import verify_token

router = APIRouter()

@router.get("/{a1id}")
async def asa_list(
    a1id: int,
    db: Session = Depends(deps.get_db),
    authorized: bool = Depends(verify_token),
):
    try:
        rank_no = []
        asa = jsonable_encoder(fetch_pools.get_asa_deets(db, a1id))
        if bool(asa) is False or authorized is False:
            raise HTTPException(status_code=401, detail="Not found")    

        rank = jsonable_encoder(list(fetch_pools.get_rank(db)))
        asa_info = jsonable_encoder(list(fetch_pools.get_asa(db, asa[0]["pool_id"])))
        for i in rank:
            if i["pool_id"] == asa[0]["pool_id"]:
                rank_no.append({"rank": i["rank"]})
        if bool(asa) is False or authorized is False:
            raise HTTPException(status_code=401, detail="Not found")
        return jsonable_encoder(list(asa)) + rank_no + asa_info
    except Exception:
        raise HTTPException(status_code=500, detail="Not found")
