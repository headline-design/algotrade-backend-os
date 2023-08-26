from typing import Optional
from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_pool, fetch_live
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.api.utils import paginationFast
from app.api.token import verify_token

router = APIRouter()


@router.get("")
def pool_asa(
    asset_id: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    favorite: bool = True,
    authorized: bool = Depends(verify_token),
):
    if (
        favorite is not True
        or authorized is False
    ):
        raise HTTPException(status_code=401, detail="Non-authorized access.")
    else:
        if "-" not in asset_id:
            try:
                validate_asset_id = fetch_live.get_asset_id(db, asset_id)
                validated_asset_id = jsonable_encoder(list(validate_asset_id)[0]["id"])
                pools = fetch_pool.with_select_as(
                        db, fetch_pool.get_favorite_pool(validated_asset_id)
                        )               
                response = {
                    "results": list(pools)
                }
                return response     
            except Exception:
                if bool(validate_asset_id) is False:                    
                    raise HTTPException(status_code=404, detail="Not found")          
        else:
            try:
                assets_list = []
                query_id = asset_id.replace("-", ", ")
                asset_id = asset_id.replace("-", " ")
                asset_id = asset_id.split()
                for i in asset_id:
                    assets_list.append(int(i))
                validate_asset_id = fetch_live.get_asset_id_list(db, assets_list)
                if len(assets_list) != len(jsonable_encoder(list(validate_asset_id))):
                    raise HTTPException(status_code=404, detail="Not found") 
                pools = fetch_pool.with_select_as(
                        db, fetch_pool.get_favorite_pool(query_id)
                        )                                           
                response = {
                    "results": list(pools)
                }
                return response
            except Exception:
                if len(assets_list) != len(jsonable_encoder(list(validate_asset_id))):
                    raise HTTPException(status_code=404, detail="Not found")                     
