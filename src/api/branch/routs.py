from typing import Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api import schemas

from utils import models
from utils.database import session
from . import controllers as cr
from api.schemas import BranchCreate

branch_router = APIRouter()

# Dependency


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


@branch_router.post('/branches', response_model=schemas.Branch)
def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    return cr.create_branch(db=db, branch=branch)


@branch_router.get('/branches', response_model=List[schemas.Branch])
def get_branches(db: Session = Depends(get_db)):
    return cr.get_branches(db=db)


@branch_router.put('/branches', response_model=schemas.Branch)
def update_branch(name: str, branch: BranchCreate, db: Session = Depends(get_db)):
    return cr.update_branch_by_name(db=db, name=name, branch=branch)


@branch_router.delete('/branches', response_model=Dict)
def delete_branch(name: str, db: Session = Depends(get_db)):
    cr.delete_branch_by_name(db=db, name=name)
    return {"message": f"Branch {name} hade been deleted"}
