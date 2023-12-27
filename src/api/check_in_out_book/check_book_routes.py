

from enum import Enum
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import schemas
from utils.database import get_db
from . import check_book_controllers as cr
from api.schemas import ItemCreate

check_book_router = APIRouter()

tags: List[str | Enum] = ["Check/Book"]


@check_book_router.post('/items/check_out/{se_id}', response_model=schemas.CheckOut, tags=tags)
def check_out(se_id: int, employee_sesa_id: int, check_out: schemas.CheckOutCreate, db: Session = Depends(get_db)):
    return cr.check_out_item(db=db, employee_sesa_id=employee_sesa_id, item_se_id=se_id, check_out=check_out)


@check_book_router.post('/items/check_in/{se_id}', response_model=schemas.CheckIn, tags=tags)
def check_in(se_id: int, employee_sesa_id: int, check_in: schemas.CheckInCreate, db: Session = Depends(get_db)):
    return cr.check_in_item(db=db, employee_sesa_id=employee_sesa_id, item_se_id=se_id, check_in=check_in)


@check_book_router.post('/items/book/{se_id}',  response_model=schemas.Book, tags=tags)
def book(se_id: int, employee_sesa_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return cr.book_item(db=db, employee_sesa_id=employee_sesa_id, item_se_id=se_id, book=book)


@check_book_router.get('/checkouts', response_model=List[schemas.CheckOut], tags=tags)
def get_check_outs(db: Session = Depends(get_db)):
    return cr.get_check_outs(db)


@check_book_router.get('/checkins', response_model=List[schemas.CheckIn], tags=tags)
def get_check_ins(db: Session = Depends(get_db)):
    return cr.get_check_ins(db)
