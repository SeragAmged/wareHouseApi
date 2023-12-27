from fastapi import HTTPException
from sqlalchemy import Column, and_
from api.item.item_controllers import get_item_by_se_id, update_item_sautes
from utils import models
from api import item, schemas
from typing import List
from sqlalchemy.orm import Session
from api.employee.employee_controllers import get_employee_by_id, get_employee_by_sesa


def book_item(db: Session, item_se_id: int, employee_sesa_id: int, book: schemas.BookCreate) -> models.Book:
    item_db = get_item_by_se_id(db, item_se_id)
    employee_db = get_employee_by_sesa(db, sesa_id=employee_sesa_id)
    if item_db and employee_db:
        if item_db.status in [models.StatusEnum.available, models.StatusEnum.calibration_due, models.StatusEnum.test_and_tag_due]:
            update_item_sautes(db, item_se_id=item_se_id,
                               statues=models.StatusEnum.booked)

            item_db.booked = True  # type: ignore
            book_db = models.Book(**book.model_dump())
            book_db.item_id = item_db.id
            book_db.employee_id = employee_db.id

            db.add(book_db)
            db.commit()
            db.refresh(book_db)
            return book_db
        else:
            raise HTTPException(
                status_code=400, detail="item is Not available")
    else:
        raise HTTPException(
            status_code=404, detail="item is Not found")


def get_item_booker(db: Session,  item_se_id: int,) -> models.Employee:
    item_db = get_item_by_se_id(db, item_se_id)
    if item_db:
        book_db = db.query(models.Book).filter(
            models.Book.item_id == item_db.id).first()
        return get_employee_by_id(db, book_db.employee_id)  # type: ignore
    else:
        raise HTTPException(
            status_code=404, detail="item is Not available")


def drop_book(db: Session, item_se_id: int):
    item_db = get_item_by_se_id(db, item_se_id)
    if item_db:
        db_book = db.query(models.Book).filter(
            models.Book.item_id == item_db.id).first()
        item_db.booked = False  # type: ignore
        db.delete(db_book)
        db.commit()
    else:
        raise HTTPException(
            status_code=404, detail="item is Not available")


def check_out_item(db: Session, item_se_id: int, check_out: schemas.CheckOutCreate, employee_sesa_id: int) -> models.CheckOut | None:
    item_db = get_item_by_se_id(db, item_se_id)
    employee_db = get_employee_by_sesa(db, sesa_id=employee_sesa_id)
    if item_db and employee_db:
        if (item_db.status in [models.StatusEnum.available, models.StatusEnum.calibration_due, models.StatusEnum.test_and_tag_due]) or ((item_db.status in [models.StatusEnum.booked]) and get_item_booker(db, item_se_id).sesa_id == employee_sesa_id):
            if item_db.status is models.StatusEnum.booked:
                drop_book(db, item_se_id)

            if check_out.company_lended:
                update_item_sautes(db, item_se_id=item_se_id,
                                   statues=models.StatusEnum.lended)
            elif check_out.work_order or check_out.jop_name:
                update_item_sautes(db, item_se_id=item_se_id,
                                   statues=models.StatusEnum.job_assigned)

            check_out_db = models.CheckOut(**check_out.model_dump())
            check_out_db.item_id = item_db.id
            check_out_db.employee_id = employee_db.id

            db.add(check_out_db)
            db.commit()
            db.refresh(check_out_db)
            return check_out_db
        else:
            raise HTTPException(
                status_code=403, detail="not authorized")
    else:
        raise HTTPException(
            status_code=404, detail="item is Not found")


def get_check_outs(db: Session, skip: int = 0, limit: int = 100) -> List[models.CheckOut]:
    return db.query(models.CheckOut).order_by(models.CheckOut.date).offset(skip).limit(limit).all()


def get_check_ins(db: Session, skip: int = 0, limit: int = 100) -> List[models.CheckIn]:
    return db.query(models.CheckIn).order_by(models.CheckIn.date).offset(skip).limit(limit).all()


def get_check_out_by_pairs(db: Session, item_se_id: int, employee_sesa_id: int) -> models.CheckOut:
    item_db = get_item_by_se_id(db, item_se_id)
    employee_db = get_employee_by_sesa(db, employee_sesa_id)
    if employee_db and item_db:
        return db.query(models.CheckOut).order_by(models.CheckOut.date).filter(and_(models.CheckOut.employee_id == employee_db.id, models.CheckOut.item_id == item_db.id, models.CheckOut.returned == False)).first()
    raise HTTPException(
        status_code=404, detail="check out not found")


def check_in_item(db: Session, item_se_id: int, check_in: schemas.CheckInCreate, employee_sesa_id: int) -> models.CheckIn:
    item_db = get_item_by_se_id(db, item_se_id)
    employee_db = get_employee_by_sesa(db, sesa_id=employee_sesa_id)
    if item_db and employee_db:
        check_out_pair_db = get_check_out_by_pairs(
            db, item_se_id, employee_sesa_id)
        if check_out_pair_db:
            check_in_db = models.CheckIn(**check_in.model_dump())
            check_in_db.item_id = item_db.id
            check_in_db.employee_id = employee_db.id
            update_item_sautes(db, item_se_id=item_se_id,
                               statues=models.StatusEnum.available)
            check_out_pair_db.returned = True  # type: ignore
            db.add(check_in_db)
            db.commit()
            db.refresh(check_in_db)
            return check_in_db
        else:
            raise HTTPException(
                status_code=400, detail="Not authorized")

    else:
        raise HTTPException(
            status_code=404, detail="item is Not found or employee")
