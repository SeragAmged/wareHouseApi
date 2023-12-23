import sys

sys.path.append(r"C:\Users\Serag Amged\Programing\fastapi\wareHouseApi\src")

from utils import models
from api import schemas
from typing import List
from sqlalchemy.orm import Session

def get_branch(db: Session, id: int) -> models.Branch | None:
    return db.query(models.Branch).filter(models.Branch.id == id).first()


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



