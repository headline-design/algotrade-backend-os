from fastapi import Request, HTTPException

def verify_token(req: Request):
    try:
        token = req.headers["Authorization"]
        if "YNWPRvGFJC4ffAupgf7T65fRYAUz" not in token:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return True
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")
