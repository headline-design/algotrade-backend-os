from typing import Optional
from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_candles
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.api.token import verify_token
from app.api.utils import paginationFastt, get_time_table

router = APIRouter()


@router.get("/{pool_id}/interval/{timeframe}")
def get_candle(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    pool_id: Optional[str] = None,
    currency: Optional[str] = None,
    timeframe: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    authorized: bool = Depends(verify_token)
):
    # def get_candlesticks(pool_id: int, timeframe: str, db: Session = Depends(get_db), authorized: bool = Depends(verify_token)):
    try:
        tf = [("1m") , ("5m"), ("15m"), ("30m"), ("1h"), ("4h"), ("12h"), ("1d")]
        c = [("algo") , ("usd")]
        verify_id = jsonable_encoder(fetch_candles.get_pool_id(db, pool_id))
        if currency not in c or timeframe not in tf or str(pool_id) not in str(verify_id[0]["pool_id"]):
            raise HTTPException(status_code=404, detail="Assets not found")
        else:
            interval = timeframe
            timeframe = get_time_table(timeframe)         
            try_count = fetch_candles.getAggregateCount(db, timeframe, pool_id)
            count = jsonable_encoder(list(try_count)[0]["count_1"])
            if count >= 100:
                count = count
            if offset is None:
                if count < 100:
                    jingoff = 0
                else:
                    jingoff = count - 100
            else:
                jingoff = offset
            if limit is None:
                if offset is None and count >= 100:
                    limit = 100
                elif offset is None and count <= 100:
                    limit = count
                elif offset == 0:
                    if count > 100:
                        limit = str(count)[-2:]
                    elif count <= 100:
                        limit = count
                elif offset is not None and count >= 100:
                    limit = 100
            if currency == "usd":
                find_candle_date = jsonable_encoder(list(fetch_candles.candlestick_in_usd(db, limit, timeframe, pool_id, jingoff)))
                return_candles = fetch_candles.joinAlgoTable(
                    db,
                    interval,
                    find_candle_date[0]['first'],
                    find_candle_date[0]['last'],
                    fetch_candles.candlesticksUsd(
                        limit, jingoff, timeframe, pool_id, find_candle_date[0]['first'], find_candle_date[0]['last'],
                    )
                )
                lol = list(return_candles)
                jingcandle = paginationFastt(count, lol, jingoff)
            if currency == "algo":
                return_candles = fetch_candles.aggregateCandles(
                    db, limit, timeframe, pool_id, jingoff
                )
                lol = list(return_candles)
                jingcandle = paginationFastt(count, lol, jingoff)                 
        if return_candles is None or authorized is False:
            raise HTTPException(status_code=401, detail="Not found")
        return jingcandle
    except Exception:
        raise HTTPException(status_code=500, detail="Not found")
