from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import traded_asa
from sqlalchemy.orm import Session
from app.api.token import verify_token

router = APIRouter()

@router.get("")
async def volume(
    db: Session = Depends(deps.get_db), authorized: bool = Depends(verify_token)
):
    try:
        most_trade = traded_asa.get_traded(db)
        traded = {"results": list(most_trade)}
        if most_trade is None or authorized is False:
            raise HTTPException(status_code=404, detail="Not found")
        return traded
    except Exception:
        raise HTTPException(status_code=500, detail="Not found")
