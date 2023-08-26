from typing import Optional
from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_candles
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.api.token import verify_token
from app.api.utils import paginationFastt

router = APIRouter()


@router.get("/{pool_id}/interval/{timeframe}/{from_}/{to_}")
def get_candle(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    pool_id: Optional[str] = None,
    timeframe: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    from_: Optional[int] = None,
    to_: Optional[int] = None,
    authorized: bool = Depends(verify_token)
):
    # def get_candlesticks(pool_id: int, timeframe: str, db: Session = Depends(get_db), authorized: bool = Depends(verify_token)):
    try:
        print(from_)
        print(to_)
        tf = [("1m") , ("5m"), ("15m"), ("30m"), ("1h"), ("4h"), ("12h"), ("1d")]
        verify_id = jsonable_encoder(fetch_candles.get_pool_id(db, pool_id))

        if timeframe not in tf or str(pool_id) not in str(verify_id[0]["pool_id"]):
            raise HTTPException(status_code=404, detail="Assets not found")
        else:
            try_count = fetch_candles.get_candle_count(db, timeframe, pool_id)
            count = jsonable_encoder(list(try_count)[0]["count_1"])
            block_round = fetch_candles.candleCount(db, pool_id)
            final_round = jsonable_encoder(list(block_round)[0]["round"])
            if count >= 320:
                count = count
            if offset is None:
                if count - 320 < 320:
                    jingoff = 0
                else:
                    jingoff = count - 320
            else:
                jingoff = offset
            if limit is None:
                if offset is None and count >= 320:
                    limit = 320
                elif offset is None and count <= 320:
                    limit = count
                elif offset == 0:
                    if count > 320:
                        limit = str(count)[-2:]
                    elif count <= 320:
                        limit = count
                elif offset is not None and count >= 320:
                    limit = 320

            return_candles = fetch_candles.candleSticks(
                db, limit, timeframe, pool_id, jingoff, final_round, from_, to_
            )
            lol = list(return_candles)
            jingcandle = paginationFastt(count, lol, jingoff, pool_id, timeframe)
            print(lol)
            print(from_, to_)
        if return_candles is None or authorized is False:
            raise HTTPException(status_code=401, detail="Not found")
        return jingcandle
    except Exception:
        raise HTTPException(status_code=500, detail="Not found")
