from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_health():
    return {"massage": "ok"}
