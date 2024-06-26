from fastapi import APIRouter

router = APIRouter(prefix="", tags=["hashcheck"], redirect_slashes=False)


@router.get("/hashcheck")
async def hashcheck() -> dict[str, str]:
    return {"message": "Hashcheck"}
