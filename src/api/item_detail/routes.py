from enum import Enum
from typing import Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import schemas
from utils.database import session
from . import controllers as cr
from api.schemas import ItemDetailCreate

item_details_router = APIRouter()

tags: List[str | Enum] = ["item details"]


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()

@item_details_router.post('/itemsDetails', response_model=schemas.ItemDetail, tags=tags)
def create_item_details(item_details: ItemDetailCreate, db: Session = Depends(get_db)):
    return cr.add_item_details(db=db, item_details=item_details)

@item_details_router.get('/itemsDetails',response_model=List[schemas.ItemDetail], tags=tags)
def get_all_item_details(db: Session = Depends(get_db)):
    return cr.get_item_details(db)