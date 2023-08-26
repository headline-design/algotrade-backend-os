from typing import Optional
from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_account
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.api.token import verify_token
from app.api.utils import paginationFasttt

router = APIRouter()


@router.get("")
def account(
    address: Optional[str] = None,
    asset: Optional[int] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    pool: Optional[str] = None,
    limit: int = 10,
    offset: Optional[int] = None,
    db: Session = Depends(deps.get_db),
    authorized: bool = Depends(verify_token),    
):
    asc = [("asset"), ("date"), ("type"), ("amount_1"), ("amount_2"), ("total_price")]
    desc = [("desc"), ("asc")]
    for_pool = "all"
    try:
        if (
            sort_by is not None
            and sort_by not in asc
            or order is not None
            and order not in desc
            or pool is not None
            and pool != for_pool
            or authorized is False            
        ):
            raise HTTPException(status_code=404, detail="Not found")
        if order is None and pool is None:
            find_acc = fetch_account.get_account(db, address)
            if bool(find_acc) is False:
                raise HTTPException(status_code=404, detail="Not found")
            if bool(find_acc) is True:
                asa_volume = fetch_account.get_volume(
                    db, jsonable_encoder(find_acc[0]["address"])
                )
                vol = {"results": list(asa_volume)}
                if asa_volume is None:
                    raise HTTPException(status_code=404, detail="Not found")
                return vol

        if pool is not None:
            if pool != for_pool:
                raise HTTPException(status_code=404, detail="Not found")
            find_acc = fetch_account.get_account(db, address)
            if bool(find_acc) is False:
                raise HTTPException(status_code=404, detail="Not found")
            if bool(find_acc) is True:
                tx_pools = fetch_account.get_account_pool(
                    db, jsonable_encoder(find_acc[0]["address"])
                )
                if tx_pools is None:
                    raise HTTPException(status_code=404, detail="Not found")
                return {"pool": jsonable_encoder(list(tx_pools))}
        if order is not None:
            if order not in desc:
                raise HTTPException(status_code=404, detail="Not found")
            find_acc = fetch_account.get_account(db, address)
            if bool(find_acc) is False:
                raise HTTPException(status_code=404, detail="Not found")
            if bool(find_acc) is True:
                poo = []
                pood = []
                tx_pools = fetch_account.get_account_pool(
                    db, jsonable_encoder(find_acc[0]["address"])
                )
                poo.append({"pool": jsonable_encoder(list(tx_pools))})
                pood.append(0)
                for i in poo[0]["pool"]:
                    pood.append(i["pool_id"])
                if asset != 0 and asset not in pood:
                    raise HTTPException(status_code=404, detail="Not found")
                else:
                    if asset == 0:
                        address = f"'{address}'"
                        txCount = fetch_account.tx_count(db, address)
                        finalcount = jsonable_encoder(list(txCount)[0]["count"])
                    if asset is not None and asset != 0:
                        address = f"'{address}' and s.pool_id = {asset}"
                        txCount = fetch_account.tx_count(db, address)
                        finalcount = jsonable_encoder(list(txCount)[0]["count"])
                    if offset is not None:
                        jingoff = offset
                    else:
                        jingoff = 0
                    if int(finalcount) >= 10:
                        limit = 10
                    elif int(finalcount) <= 10:
                        limit = finalcount
                    if int(finalcount) - jingoff <= 10:
                        limit = int(finalcount) - jingoff
                    asa_volume = fetch_account.get_account_tx(
                        db,
                        address,
                        sort_by,
                        order,
                        limit,
                        jingoff,
                    )

                    vol = paginationFasttt(
                        finalcount, asa_volume, jingoff, limit
                    )
                    if asa_volume is None:
                        raise HTTPException(status_code=404, detail="Not found")
                    return vol
    except Exception:
        raise HTTPException(status_code=500, detail="Not found")
