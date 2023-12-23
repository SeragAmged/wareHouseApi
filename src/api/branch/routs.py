import re
from fastapi import APIRouter, HTTPException
from msilib import schema
from utils.database import session
from . import controllers as cr
from api.schemas import BranchCreate

from api import branch
branch_router = APIRouter()

# Dependency


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


@branch_router.get('/branches')
def get_branches():
    return cr.get_branches(db=session)


@branch_router.post('/branches')
def create_branch(branch: BranchCreate):
    return cr.create_branch(db=session, branch=branch)


@branch_router.delete('/branches')
def delete_branch(name: str):
    cr.delete_branch_by_name(db=session, name=name)
    return {"message": f"Branch {name} hade been deleted"}
