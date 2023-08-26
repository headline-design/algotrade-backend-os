from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_hdl_price
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.api.token import verify_token

router = APIRouter()


@router.get("")
def get_hdl_price(
    skip: int = 0,
    db: Session = Depends(deps.get_db),
    authorized: bool = Depends(verify_token),
):
    try:
        candle_query = fetch_hdl_price.fetch_latest(db)
        response = jsonable_encoder(list(candle_query))
        if candle_query is None or authorized is False:
            raise HTTPException(status_code=401, detail="Not found")
        return response
    except Exception:
        raise HTTPException(status_code=500, detail="Not found")
