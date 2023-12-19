import sys

sys.path.append(r"C:\Users\Serag Amged\Programing\fastapi\wareHouseApi\src")

from utils import models
from api import schemas
from typing import List
from sqlalchemy.orm import Session
from utils.database import session

def get_branch(db: Session, branch_id: int) -> models.Branch | None:
    return db.query(models.Branch).filter(models.Branch.id == branch_id).first()


def get_branch_by_name(db: Session, name: str) -> models.Branch | None:
    return db.query(models.Branch).filter(models.Branch.name == name).first()


def get_branches(db: Session, skip: int = 0, limit: int = 100) -> List[models.Branch]:
    return db.query(models.Branch).offset(skip).limit(limit).all()


def create_branch(db: Session, branch: schemas.BranchCreate):
    db_branch = models.Branch(name=branch.name)
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch


my_branch :schemas.BranchCreate = schemas.BranchCreate(name="west")
create_branch(db=session,branch=my_branch)

# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
