from enum import Enum
from typing import Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import schemas
from utils.database import get_db
from . import controllers as cr
from api.schemas import ItemDetailCreate

item_details_router = APIRouter()

tags: List[str | Enum] = ["item details"]


@item_details_router.post('/itemsDetails', response_model=schemas.ItemDetail, tags=tags)
async def create(item_detail: ItemDetailCreate, db: Session = Depends(get_db)):
    return cr.add_item_detail(db=db, item_detail=item_detail)


@item_details_router.get('/itemsDetails', response_model=List[schemas.ItemDetail], tags=tags)
async def get_all(db: Session = Depends(get_db)):
    return cr.get_item_details(db)


@item_details_router.put('/itemsDetails/{name}', response_model=schemas.ItemDetail, tags=tags)
async def update(item_detail: ItemDetailCreate, name: str, db: Session = Depends(get_db)):
    return cr.update_item_detail(db=db, new_item_detail=item_detail, target_name=name)
