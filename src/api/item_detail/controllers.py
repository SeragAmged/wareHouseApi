from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from utils import models
from api import schemas


def get_item_details(db: Session, skip: int = 0, limit: int = 100) -> list[models.ItemDetail] | None:
    return db.query(models.ItemDetail).order_by(models.ItemDetail.name).offset(skip).limit(limit).all()


def get_item_detail_by_id(db: Session, id: int) -> models.ItemDetail | None:

    return db.query(models.ItemDetail).filter(models.ItemDetail.id == id).first()


def get_item_detail_by_name(db: Session, name: str) -> models.ItemDetail | None:

    return db.query(models.ItemDetail).filter(models.ItemDetail.name == name).first()


def validate_Item_detail(db: Session, name: str):
    if get_item_detail_by_name(db, name):
        raise HTTPException(
            status_code=400, detail="Item with the same name already exists.")


def add_item_detail(db: Session, item_detail: schemas.ItemDetailCreate) -> models.ItemDetail | None:
    # Create a new ItemDetail instance and add it to the database

    validate_Item_detail(db, item_detail.name)

    db_item_details = models.ItemDetail(**item_detail.model_dump())
    db.add(db_item_details)
    db.commit()
    db.refresh(db_item_details)
    return db_item_details


def update_item_detail(db: Session, target_name: str, new_item_detail: schemas.ItemDetailCreate) -> models.ItemDetail | None:
    validate_Item_detail(db, new_item_detail.name)
    
    if get_item_detail_by_name(db, target_name) is None:
        raise HTTPException(
            status_code=404, detail="Item not found.")
        
    db_item_detail_update = get_item_detail_by_name(db, target_name)
    for key, value in new_item_detail.model_dump().items():
        setattr(db_item_detail_update, key, value)
    db.commit()
    db.refresh(db_item_detail_update)
    return db_item_detail_update


