from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def read_root():
    return {"Hello": "World"}


@router.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    return router.openapi()
