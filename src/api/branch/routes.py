from enum import Enum
from typing import Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import schemas
from utils.database import session
from . import controllers as cr
from api.schemas import BranchCreate

router = APIRouter()

tags: List[str | Enum] = ["branch"]

def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


@router.post('/branches', response_model=schemas.Branch, tags=tags)
def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    return cr.create_branch(db=db, branch=branch)


@router.get('/branches', response_model=List[schemas.Branch], tags=tags)
def get_branches(db: Session = Depends(get_db)):
    return cr.get_branches(db=db)


@router.put('/branches', response_model=schemas.Branch, tags=tags)
def update_branch(name: str, branch: BranchCreate, db: Session = Depends(get_db),):
    return cr.update_branch_by_name(db=db, name=name, branch=branch)


@router.delete('/branches', response_model=Dict, tags=tags)
def delete_branch(name: str, db: Session = Depends(get_db)):
    cr.delete_branch_by_name(db=db, name=name)
    return {"message": f"Branch {name} hade been deleted"}
