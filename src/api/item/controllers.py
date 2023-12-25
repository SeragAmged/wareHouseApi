from fastapi import HTTPException
from utils import models
from api import schemas
from typing import List
from sqlalchemy.orm import Session
from api.branch.controllers import get_branch_by_name
from api.item_detail.controllers import get_item_details_by_name
from api.employee.controllers import get_employee_by_sesa



#Add Item 

def add_item_record(db:Session,item_record:schemas.ItemRecordCreate) -> models.ItemRecord | None:
    db_item_record = models.ItemRecord(**item_record.model_dump())
    db.add(db_item_record)
    db.commit()
    db.refresh(db_item_record)

def add_item(db:Session,item:schemas.ItemCreate):
    #check Validity of Data
    item_details = get_item_details_by_name(db,item.item_detail_name)
    branch=get_branch_by_name(db,item.branch_name)
    employee=get_employee_by_sesa(db,item.employee_sesa_id)
    
    if item_details is None or branch is None or employee is None:
        raise HTTPException(status_code=404, detail="item details or branch or employee is Not found")
    
    item_details[0].quantity=item_details[0].quantity +1
    db.commit()
    db.refresh(item_details)
    item.branch_id=branch[0].id
    item.item_detail_id=item_details[0].id
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    #Add Item Record 
    add_item_record(db,schemas.ItemRecordCreate(employee_id=employee[0].id,item_id=db_item[0].id,
                                                type=models.OperationTypesEnum.create))
    return db_item

def get_item_by_se_id(db:Session,item_se_id:int) -> models.Item | None:
    return db.query(models.Item).filter(models.Item.serial_number==item_se_id).first()

def update_item_sautes(db:Session,statues:models.StatusEnum,item_se_id:int) -> models.Item | None:
    item= get_item_by_se_id(db,item_se_id)
    if item is None:
         raise HTTPException(status_code=404, detail="item is Not found")
    item[0].status=statues
    db.commit()
    db.refresh(item)






# NOTE: DONT FORGET TO UPDATE STATUS IF NEEDED
# NOTE: admin and user is only for routs

# TODO:

# ONLY FOR ADMINS

# Add item
# Adding new item depends on itemdetail name not id
# also add records for it with type from the enums

# delete item with se_id
# also add records for it with type from the enums

# update item with se_id
# also add records for it with type from the enums

#update Item status

# update item book
# update item comment



# read item records
# read item check-ins
# read item check-outs
# ------------------------------ #


# sys (no routs)
# get item by id

# USER ROUTS

# when get items list it with its itemdetail (NOTE)
# get item by se_id


# get item comments using se_id and display the employee name(first, last) of each comment , sesa_id and rule if admin

# if items is jop assigned out return employee assigner
# if items is booked out return employee booker and book details