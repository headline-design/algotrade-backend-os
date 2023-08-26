from typing import Optional
from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_live, fetch_account
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.api.utils import paginationFastttt, paginationFasttt
from app.api.token import verify_token

router = APIRouter()


@router.get("/{pool_id}")
def pool_asa(
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    pool_id: Optional[int] = None,
    offset: Optional[int] = None,
    address: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    authorized: bool = Depends(verify_token),    
):
    try:
        maxx = [10]
        asc = [
            ("date"),
            ("round"),
            ("swap_type"),
            ("type"),
            ("amount_1"),
            ("amount_2"),
            ("excess"),
            ("amount_1_final"),
            ("amount_2_final"),
            ("total_price"),
            ("address"),
        ]
        desc = [("desc"), ("asc")]

        if (
            sort_by not in asc
            or order not in desc
            or limit not in maxx
            or authorized is False            
        ):
            raise HTTPException(status_code=404, detail="Not found")
        else:
            try:
                if address is not None:
                    find_acc = fetch_account.get_account(db, address)
                    if bool(find_acc) is False:
                        raise HTTPException(status_code=404, detail="Not found")                    
                    else:
                        pools = fetch_live.get_pool_id(db, pool_id)
                        pid = jsonable_encoder(list(pools)[0]["pool_id"])
                        if pid != pool_id:
                            raise HTTPException(status_code=404, detail="Not found")
                        else:
                            count = fetch_live.tx_count_account(db, pool_id, jsonable_encoder(find_acc[0]["address"]))
                            fcount = jsonable_encoder(list(count)[0]["count_1"])
                            if offset is not None:
                                jingoff = offset
                            else:
                                jingoff = 0
                            if int(fcount) >= 10:
                                limit = 10
                            elif int(fcount) <= 10:
                                limit = fcount
                            if int(fcount) - jingoff <= 10:
                                limit = int(fcount) - jingoff
                            # elif int(fcount) <= 25:
                            #     limit = fcount
                            if sort_by == 'date' and order == 'desc':
                                sort_by = 'date desc, intra'
                            if sort_by == 'date' and order == 'asc':
                                sort_by = 'date asc, intra'
                            trades = fetch_live.liveTxAccount(db, limit, pid, jingoff, sort_by, order, jsonable_encoder(find_acc[0]["address"]))
                            asa_pair = paginationFasttt(
                                fcount, trades, jingoff, limit
                            )             
                            return asa_pair
                if address is None:
                    pools = fetch_live.get_pool_id(db, pool_id)
                    pid = jsonable_encoder(list(pools)[0]["pool_id"])
                    if pid != pool_id:
                        raise HTTPException(status_code=404, detail="Not found")
                    else:
                        count = fetch_live.tx_count(db, pool_id)
                        fcount = jsonable_encoder(list(count)[0]["count_1"])
                        percent = fetch_live.percentage_tx(db, pid)
                        if offset is not None:
                            jingoff = offset
                        else:
                            jingoff = 0
                        if int(fcount) >= 10:
                            limit = 10
                        elif int(fcount) <= 10:
                            limit = fcount
                        if int(fcount) - jingoff <= 10:
                            limit = int(fcount) - jingoff
                        # elif int(fcount) <= 25:
                        #     limit = fcount
                        if sort_by == 'date' and order == 'desc':
                            sort_by = 'date desc, intra'
                        if sort_by == 'date' and order == 'asc':
                            sort_by = 'date asc, intra'
                        trades = fetch_live.liveTx(db, limit, pid, jingoff, sort_by, order)
                        asa_pair = paginationFastttt(
                            fcount, trades, jingoff, limit, jsonable_encoder(list(percent)[0])
                        )
                        return asa_pair
            except Exception:
                raise HTTPException(status_code=404, detail="Not found")

    except Exception:
        raise HTTPException(status_code=500, detail="Not found")
