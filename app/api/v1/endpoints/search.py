from fastapi import APIRouter, Depends, Depends, HTTPException
from app.api import deps
from app.fetch import fetch_search
from sqlalchemy.orm import Session
from app.api.token import verify_token

router = APIRouter()


@router.get("")
def asa_search(
    db: Session = Depends(deps.get_db),
    authorized: bool = Depends(verify_token),
):
    try:
        asa = fetch_search.get_search(db)
        if asa is None or authorized is False:
            raise HTTPException(status_code=404, detail="Not found")
        return list(asa)
    except Exception:
        raise HTTPException(status_code=404, detail="Not found")
