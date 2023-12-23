from fastapi import HTTPException
from utils import models
from api import schemas
from typing import List
from sqlalchemy.orm import Session

# read


def get_branch_by_id(db: Session, id: int) -> models.Branch | None:
    return db.query(models.Branch).filter(models.Branch.id == id).first()


def get_branch_by_name(db: Session, name: str) -> models.Branch | None:
    return db.query(models.Branch).filter(models.Branch.name == name).first()


def get_branches(db: Session, skip: int = 0, limit: int = 100) -> List[models.Branch]:
    return db.query(models.Branch).order_by(models.Branch.name).offset(skip).limit(limit).all()


# create
def create_branch(db: Session, branch: schemas.BranchCreate) -> models.Branch:
    if get_branch_by_name(db=db, name=branch.name):
        raise HTTPException(status_code=400, detail="Branch is already added")
    
    db_branch = models.Branch(**branch.model_dump())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch


def delete_branch_by_name(db: Session, name: str) -> None:
    if get_branch_by_name(db=db, name=name) is None:
        raise HTTPException(status_code=400, detail="Branch is not in database")
    
    db_branch = db.query(models.Branch).filter(
        models.Branch.name == name).first()
    db.delete(db_branch)
    db.commit()


def update_branch(db: Session, branch_id: int, branch: schemas.BranchCreate):
    db_branch_update = db.query(models.Branch).filter(
        models.Branch.id == branch_id).first()
    for key, value in branch.model_dump().items():
        setattr(db_branch_update, key, value)
    db.commit()
    db.refresh(db_branch_update)
    return db_branch_update
