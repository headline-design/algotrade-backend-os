from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_recently_added
from sqlalchemy.orm import Session
from app.api.token import verify_token

router = APIRouter()


@router.get("")
def volume(
    db: Session = Depends(deps.get_db), authorized: bool = Depends(verify_token)
):
    try:
        asa_volume = fetch_recently_added.get_recently_added(db)
        vol = {"results": list(asa_volume)}
        if asa_volume is None or authorized is False:
            raise HTTPException(status_code=404, detail="Not found")
        return vol
    except Exception:
        raise HTTPException(status_code=500, detail="Not found")
