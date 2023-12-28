from enum import Enum
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import schemas
from utils.database import get_db
from . import item_controllers as cr
from api.schemas import ItemCreate

item_router = APIRouter()

tags: List[str | Enum] = ["item"]


@item_router.post('/items', response_model=schemas.Item, tags=tags)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return cr.add_item(db=db, item=item)



@item_router.get('/items/', response_model=List[schemas.Item], tags=tags)
async def get_items_router(db: Session = Depends(get_db)):
    return cr.get_items(db=db)


@item_router.put('/items/{item_se_id}', response_model=schemas.Item, tags=tags)
async def update(item: ItemCreate, item_se_id: int, db: Session = Depends(get_db)):
    return cr.update_item_by_Se_id(db=db, item=item, item_se_id=item_se_id)



@item_router.get('/items/{branch_name}/pdf')
def generate_report(branch_name: str, db: Session = Depends(get_db)):
    # inventory_report = cr.get_inventory_report(db, branch_name=branch_name)  # type: ignore
    # cr.create_pdf_report(inventory_report)
    # return {"message": "report generated"}
    return cr.get_inventory_report(db, branch_name=branch_name)


@item_router.get('/items/{item_se_id}',response_model=schemas.Item, tags=tags)
async def get_item(item_se_id: int, db: Session = Depends(get_db)):
    return cr.get_item_by_se_id(db,item_se_id)
    