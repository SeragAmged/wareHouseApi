from enum import Enum
from typing import Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import schemas
from utils.database import session
from . import controllers as cr
from api.schemas import ItemCreate

item_router = APIRouter()

tags: List[str | Enum] = ["item"]


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()

@item_router.post('/items', response_model=schemas.Item, tags=tags)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return cr.add_item(db=db, item=item)

@item_router.get('/items/records', response_model=List[schemas.ItemRecord], tags=tags)
def get_itemR(db: Session = Depends(get_db)):
    return cr.get_item_records(db=db)