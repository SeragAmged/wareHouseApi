from tkinter.messagebox import NO
from fastapi import HTTPException
from utils import models
from api import schemas
from typing import List
from sqlalchemy.orm import Session

# read


def get_branch_by_id(db: Session, id: int) -> models.Branch | None:
    return db.query(models.Branch).filter(models.Branch.id == id).first()


def get_branch_by_name(db: Session, name: str) -> models.Branch | None:
    """reruns branch by name

    Args:
        db (Session): SQLAlchemy database session.
        name (str): branch name

    Returns:
        models.Branch | None: branch if there
    """
    return db.query(models.Branch).filter(models.Branch.name == name).first()


def get_branches(db: Session, skip: int = 0, limit: int = 100) -> List[models.Branch]:
    """returns all branches

    Args:
        db (Session): SQLAlchemy database session.
        skip (int, optional): page skipped Defaults to 0.
        limit (int, optional): limit in the page Defaults to 100.

    Returns:
        List[models.Branch]: _description_
    """
    return db.query(models.Branch).order_by(models.Branch.name).offset(skip).limit(limit).all()


# create
def create_branch(db: Session, branch: schemas.BranchCreate) -> models.Branch:
    """creates a new branch if it was not in the db

    Args:
        db (Session):SQLAlchemy database session.
        branch (schemas.BranchCreate): the new branch

    Raises:
        HTTPException: if branch is already in db

    Returns:
        models.Branch: created branch
    """
    if get_branch_by_name(db=db, name=branch.name):
        raise HTTPException(status_code=400, detail="Branch is already added")

    db_branch = models.Branch(**branch.model_dump())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch


def delete_branch_by_name(db: Session, name: str) -> None:
    """deletes branch by name

    Args:
        db (Session): SQLAlchemy database session.
        name (str): name of the branch.

    Raises:
        HTTPException: Branch is not in found if not found
    Do:
        delete the wanted branch
    """
    if get_branch_by_name(db=db, name=name) is None:
        raise HTTPException(
            status_code=400, detail="Branch is not in found")

    db_branch = db.query(models.Branch).filter(
        models.Branch.name == name).first()
    db.delete(db_branch)
    db.commit()


def update_branch_by_name(db: Session, name: str, branch: schemas.BranchCreate) -> models.Branch:
    """
    update branch name by branch name.

    Args:
        db (Session): SQLAlchemy database session.
        name (str): name of the branch.

    Returns:
       models.Branch: updated branch
        
    """
    db_branch_update = get_branch_by_name(db=db, name=name)

    if db_branch_update is None:
        raise HTTPException(
            status_code=400, detail="Branch is not found")

    if get_branch_by_name(db=db, name=branch.name):
        raise HTTPException(
            status_code=400, detail="Branch name is already used")

    for key, value in branch.model_dump().items():
        setattr(db_branch_update, key, value)
    db.commit()
    db.refresh(db_branch_update)
    return db_branch_update


def get_branch_employees(db: Session, branch_name: str) -> List[models.Employee]:
    """
    Get a list of employees for the given branch name.

    Args:
        db (Session): SQLAlchemy database session.
        branch_name (str): name of the branch.

    Returns:
        List[Employee]: List of employees associated with the branch.
    """
    test_branch = get_branch_by_name(db=db, name=branch_name)
    if test_branch is not None:
        branch_id = test_branch.id
        employees = db.query(models.Employee).filter(
            models.Employee.branch_id == branch_id).all()
        return employees
    else:
        raise HTTPException(
            status_code=400, detail="Branch name is not found")




def get_branch_items(db: Session, branch_name: str) -> List[models.Item]:
    """
    Get a list of items for the given branch name.

    Args:
        db (Session): SQLAlchemy database session.
        branch_name (str): name of the branch.

    Returns:
        List[Item]: List of items associated with the branch.
    """
    test_branch = get_branch_by_name(db=db, name=branch_name)
    if test_branch is not None:
        branch_id = test_branch.id
        items = db.query(models.Item).filter(
            models.Employee.branch_id == branch_id).all()
        return items
    else:
        raise HTTPException(
            status_code=400, detail="Branch name is not found")


# TODO:
# get branch items by branch name (list all items in branch x)
