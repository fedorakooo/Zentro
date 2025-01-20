from fastapi import APIRouter

router = APIRouter(tags=["Items"])

@router.get("/")
def read_items():
        return {}
