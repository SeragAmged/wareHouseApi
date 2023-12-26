from enum import Enum
from typing import Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import schemas
from utils.database import get_db
from . import branch_controllers as cr
from api.schemas import BranchCreate

branch_router = APIRouter()

tags: List[str | Enum] = ["branch"]


@branch_router.post('/branches', response_model=schemas.Branch, tags=tags)
def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    return cr.add_branch(db=db, branch=branch)


@branch_router.get('/branches', response_model=List[schemas.Branch], tags=tags)
def get_branches(db: Session = Depends(get_db)):
    return cr.get_branches(db=db)


@branch_router.get('/branchEmployees/{name}', response_model=Dict[str, List[schemas.Employee]], tags=tags)
def get_branch_employees(name: str, db: Session = Depends(get_db)):
    return {"employees": cr.get_branch_employees(db=db, branch_name=name)}


@branch_router.get('/branchItems/{name}', response_model=Dict[str, List[schemas.Item]], tags=tags)
def get_branch_Items(name: str, db: Session = Depends(get_db)):
    return {"items": cr.get_branch_items(db=db, branch_name=name)}


@branch_router.put('/branches/{name}', response_model=schemas.Branch, tags=tags)
def update_branch(name: str, branch: BranchCreate, db: Session = Depends(get_db),):
    return cr.update_branch_by_name(db=db, name=name, branch=branch)


@branch_router.delete('/branches', response_model=Dict, tags=tags)
def delete_branch(name: str, db: Session = Depends(get_db)):
    cr.delete_branch_by_name(db=db, name=name)
    return {"message": f"Branch {name} hade been deleted"}
