from fastapi import APIRouter, Depends, Depends, HTTPException
from api import deps
from fetch import fetch_algo
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.token import verify_token
router = APIRouter()


@router.get("")
def get_algo(db: Session = Depends(deps.get_db), authorized: bool = Depends(verify_token)):

    candle_query = fetch_algo.fetch_algorand(db)
    response = {
        "response": jsonable_encoder(list(candle_query))
    }
    if candle_query is None or authorized is False:
        raise HTTPException(status_code=404, detail="User not found")
    
    return response