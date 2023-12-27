from fastapi import HTTPException
from sqlalchemy import and_

from utils import models
from api import schemas
from typing import List
from sqlalchemy.orm import Session
from api.branch.branch_controllers import get_branch_by_name
from api.item_detail.item_detail_controllers import get_item_detail_by_name
from api.employee.employee_controllers import get_employee_by_sesa
from sqlalchemy import func
from reportlab.pdfgen import canvas


# Add Item


def get_item_by_id(db: Session, item_id: int) -> models.Item | None:
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_item_by_se_id(db: Session, item_se_id: int) -> models.Item | None:
    return db.query(models.Item).filter(models.Item.se_id == item_se_id).first()


def get_by_serial(db: Session, item_serial_number: int) -> models.Item | None:
    return db.query(models.Item).filter(models.Item.serial_number == item_serial_number).first()


def validate_item_exist(db: Session, item: schemas.ItemCreate):
    if get_item_by_se_id(db, item.se_id):
        raise HTTPException(status_code=400, detail="se_id is already used")
    if get_by_serial(db, item.serial_number):
        raise HTTPException(status_code=400, detail="serial is already used")


def validate_item_new(db: Session, item: schemas.ItemCreate) -> bool:
    if get_item_by_se_id(db, item.se_id) is None and get_by_serial(db, item.serial_number) is None:
        return True
    else:
        return False


def get_items_by_name(db: Session, name: str) -> List[models.Item]:
    db_item_details = get_item_detail_by_name(db=db, name=name)
    if db_item_details is not None:
        return db.query(models.Item).order_by(models.Item.se_id).filter(models.Item.item_detail_id == db_item_details.id).all()
    else:
        raise HTTPException(status_code=404, detail="item is Not found")


def get_items(db: Session, skip: int = 0, limit: int = 100) -> list[models.Item]:
    return db.query(models.Item).order_by(models.Item.se_id).offset(skip).limit(limit).all()


def update_item_sautes(db: Session, statues: models.StatusEnum, item_se_id: int) -> models.Item | None:
    item = get_item_by_se_id(db, item_se_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item is Not found")
    else:
        item.status = statues  # type: ignore
        db.commit()
        db.refresh(item)


def add_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    validate_item_exist(db, item)
    # check Validity of Data
    item_details = get_item_detail_by_name(db, item.item_detail_name)
    branch = get_branch_by_name(db, item.branch_name)

    if item_details is None:
        raise HTTPException(
            status_code=404, detail="item details  is Not found")
    if branch is None:
        raise HTTPException(status_code=404, detail="branch is Not found")

    dumb_item = item.model_dump()
    dumb_item['branch_id'] = branch.id
    dumb_item['item_detail_id'] = item_details.id

    item_details.quantity += len(get_items_by_name(db=db,  # type: ignore
                                 name=dumb_item['item_detail_name'])) + 1
    del dumb_item['item_detail_name']
    del dumb_item['branch_name']
    db_item = models.Item(**dumb_item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def update_item_by_Se_id(db: Session, item_se_id: int, item: schemas.ItemCreate) -> models.Item:

    db_item_update = get_item_by_se_id(db, item_se_id)
    if db_item_update:
        if (validate_item_new(db, item)):
            # check Validity of Data
            item_details = get_item_detail_by_name(db, item.item_detail_name)
            branch = get_branch_by_name(db, item.branch_name)

            if item_details is None:
                raise HTTPException(
                    status_code=404, detail="item detail name is Not found")
            if branch is None:
                raise HTTPException(
                    status_code=404, detail="branch is Not found")

            for key, value in item.model_dump().items():
                if key in ['item_detail_id', 'branch_id', 'se_id', 'serial_number']:
                    continue
                else:
                    setattr(db_item_update, key, value)
            db.commit()
            db.refresh(db_item_update)
            return db_item_update
        else:
            raise HTTPException(
                status_code=400, detail="new item se id  or serial is used")
    else:
        raise HTTPException(
            status_code=404, detail="item se_id  is Not found")




def get_inventory_report(db: Session, branch_name: str):
    branch_db = get_branch_by_name(db, branch_name)
    # Query to get overall inventory and stock levels
    if branch_db:
        result = db.query(
            models.Branch.name,
            func.count(models.Item.id).label('total_items'),
        ).join(models.Item, models.Branch.id == models.Item.branch_id).group_by(models.Branch.name).all()
        return result


def create_pdf_report(inventory_data, filename='inventory_report.pdf'):
    pdf = canvas.Canvas(filename)

    # Set up PDF title and headers
    pdf.setFont("Helvetica", 16)
    pdf.drawString(100, 800, "Inventory Report")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 780, "Branch Name")
    pdf.drawString(250, 780, "Total Items")
    pdf.drawString(400, 780, "Total Quantity")

    # Add data to the PDF
    y_position = 760
    for row in inventory_data:
        pdf.drawString(100, y_position, row.branch_name)
        pdf.drawString(250, y_position, str(row.total_items))
        pdf.drawString(400, y_position, str(row.total_quantity))
        y_position -= 20

    pdf.save()


# if _name_ == "_main_":
#     from database import get_db

#     # Example of how to use the get_inventory_report function
#     inventory_report = get_inventory_report(db)

#     # Create and save PDF report
#     create_pdf_report(inventory_report)
#     print("PDF report created and saved as 'inventory_report.pdf'")

# NOTE: DONT FORGET TO UPDATE STATUS IF NEEDED(Check-out,in, book)

# TODO:

# ONLY FOR ADMINS
# authenticate Add item
# update item book
# update item comment
# ------------------------------ #


# USER ROUTS

# create comment
# book item if it's available


# get item comments using se_id and display the employee name(first, last) of each comment , sesa_id and rule if admin


# DONT DO!!!!!!!!!!!
# if items is jop assigned out return employee assigner
# if items is booked out return employee booker and book details
