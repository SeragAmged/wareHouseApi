from typing import List
from sqlalchemy.orm import Session
from utils import models


def get_item_detail(db: Session, id: int) -> models.ItemDetail | None:
    return db.query(models.ItemDetail).filter(models.ItemDetail.id == id).first()


def get_branch_by_name(db: Session, name: str) -> models.ItemDetail | None:
    return db.query(models.ItemDetail).filter(models.ItemDetail.name == name).first()


def get_branches(db: Session, skip: int = 0, limit: int = 100) -> List[models.Branch]:
    return db.query(models.Branch).offset(skip).limit(limit).all()


# add itemDetail
# also add records for it

# delete itemDetail

# also add records for it

# update itemDetail
# also add records for it

# get itemdetail by name

