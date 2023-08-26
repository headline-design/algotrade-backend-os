from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_assets
from sqlalchemy.orm import Session
from app.api.token import verify_token

router = APIRouter()

@router.get("/")
def asa_list(
    db: Session = Depends(deps.get_db), authorized: bool = Depends(verify_token)
):
    try:
        asa = fetch_assets.get_asset_id(db)
        if asa is None or authorized is False:
            raise HTTPException(status_code=401, detail="Not found")
        return list(asa)
    except Exception:
        raise HTTPException(status_code=500, detail="Not found")
