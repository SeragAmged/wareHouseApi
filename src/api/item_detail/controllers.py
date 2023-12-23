from typing import List
from sqlalchemy.orm import Session
from utils import models
import sys
sys.path.append(r"C:\Users\Serag Amged\Programing\fastapi\wareHouseApi\src")


def get_item_detail(db: Session, id: int) -> models.ItemDetail | None:
    return db.query(models.ItemDetail).filter(models.ItemDetail.id == id).first()


def get_branch_by_name(db: Session, name: str) -> models.ItemDetail | None:
    return db.query(models.ItemDetail).filter(models.ItemDetail.name == name).first()


def get_branches(db: Session, skip: int = 0, limit: int = 100) -> List[models.Branch]:
    return db.query(models.Branch).offset(skip).limit(limit).all()