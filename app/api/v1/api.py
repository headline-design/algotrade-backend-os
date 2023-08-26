from fastapi import APIRouter

from app.api.v1.endpoints import (
    account,
    mostasa,
    volume,
    pool,
    algo,
    candles,
    asa,
    asa_pool,
    livetx,
    search,
    algo_latest,
    home,
    asa_pairs,
    post_asa,
    nth,
    hdl_price,
    assets_sparkline,
    winner,
    favorite_pool,
    assets_view,
    recently_added
)


api_router = APIRouter()
api_router.include_router(mostasa.router, prefix="/most-traded-asa", tags=["users"])
api_router.include_router(volume.router, prefix="/asa-volume", tags=["users"])
api_router.include_router(pool.router, prefix="/pool-assets")
api_router.include_router(algo.router, prefix="/algorandforthewin")
api_router.include_router(algo_latest.router, prefix="/latest")
api_router.include_router(candles.router, prefix="/candles")
api_router.include_router(asa.router, prefix="/asa")
api_router.include_router(asa_pool.router, prefix="/asa-pools")
api_router.include_router(livetx.router, prefix="/live-trades")
api_router.include_router(search.router, prefix="/search")
api_router.include_router(account.router, prefix="/account")
api_router.include_router(home.router, prefix="/home")
api_router.include_router(asa_pairs.router, prefix="/asa-pairs")
api_router.include_router(post_asa.router, prefix="/asa_info")
api_router.include_router(nth.router, prefix="/nth")
api_router.include_router(winner.router, prefix="/biggest-gainers")
api_router.include_router(hdl_price.router, prefix="/hdl-latest")
api_router.include_router(assets_sparkline.router, prefix="/sparkline-7d")
api_router.include_router(favorite_pool.router, prefix="/favorite-assets")
api_router.include_router(recently_added.router, prefix="/recently-added")
api_router.include_router(assets_view.router, prefix="/assets-view")

