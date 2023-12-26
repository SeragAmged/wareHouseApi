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


@item_router.post('/items/check_out/{se_id}', response_model=schemas.CheckOut, tags=tags)
def check_out(se_id: int, employee_sesa_id: int, check_out: schemas.CheckOutCreate, db: Session = Depends(get_db)):
    return cr.check_out_item(db=db, employee_sesa_id=employee_sesa_id, item_se_id=se_id, check_out=check_out)


@item_router.post('/items/check_in/{se_id}', response_model=schemas.CheckIn, tags=tags)
def check_in(se_id: int, employee_sesa_id: int, check_in: schemas.CheckInCreate, db: Session = Depends(get_db)):
    return cr.check_in_item(db=db, employee_sesa_id=employee_sesa_id, item_se_id=se_id, check_in=check_in)


@item_router.get('/items/', response_model=List[schemas.Item], tags=tags)
async def get_items_router(db: Session = Depends(get_db)):
    return cr.get_items(db=db)


@item_router.put('/items/{item_se_id}', response_model=schemas.Item, tags=tags)
async def update(item: ItemCreate, item_se_id: int, db: Session = Depends(get_db)):
    return cr.update_item_by_Se_id(db=db, item=item, item_se_id=item_se_id)


@item_router.get('/checkouts', response_model=List[schemas.CheckOut], tags=["check-outs"])
def get_check_outs(db: Session = Depends(get_db)):
    return cr.get_check_outs(db)


@item_router.get('/checkins', response_model=List[schemas.CheckIn], tags=["check-ins"])
def get_check_ins(db: Session = Depends(get_db)):
    return cr.get_check_ins(db)


@item_router.get('/items/{branch_name}/pdf')
def generate_report(branch_name: str, db: Session = Depends(get_db)):
    # inventory_report = cr.get_inventory_report(db, branch_name=branch_name)  # type: ignore
    # cr.create_pdf_report(inventory_report)
    # return {"message": "report generated"}
    return cr.get_inventory_report(db, branch_name=branch_name)
