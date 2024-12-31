from fastapi import APIRouter

router = APIRouter(tags=["items"])

@router.get("/")
def read_items():
        return {}
