from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_assets_view, fetch_pools
from sqlalchemy.orm import Session
from app.api.token import verify_token
from datetime import datetime, timezone
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("")
def asa_list(
    asset_id: int,
    reason: str,
    db: Session = Depends(deps.get_db),
    authorized: bool = Depends(verify_token),
):
    try:
        dt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        asa = jsonable_encoder(fetch_pools.getAsaId(db, asset_id))
        if bool(asa) is False:
            raise HTTPException(status_code=404, detail="Not found")     
        else:
            z = fetch_assets_view.insert_view(
                db, asa[0]["asset_1_id"], dt, reason
            )
            result = {
                "current_view": jsonable_encoder(list(z))[0]['current_view']
            }
            return jsonable_encoder(result)
    except Exception:
        raise HTTPException(status_code=404, detail="Not found")
