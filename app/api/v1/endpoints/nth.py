from fastapi import APIRouter
router = APIRouter()

@router.get("")
def get_algo(
):
    z = 'hi'
    return z
