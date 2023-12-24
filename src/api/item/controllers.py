from fastapi import HTTPException
from utils import models
from api import schemas
from typing import List
from sqlalchemy.orm import Session
from api.branch.controllers import get_branch_by_name
from api.item_detail.controllers import get_item_details_by_name



#Add Item 

def create_item_record(db:Session):
    pass

def add_item(db:Session,item:schemas.ItemCreate):
    item_details = get_item_details_by_name(db,item.item_detail_name)
    branch=get_branch_by_name(db,item.branch_name)
    if item_details is None or branch is None :
        raise HTTPException(status_code=400, detail="item details or branch is Not found")
    else:
        item.branch_id=branch[0].id
        item.item_detail_id=item_details[0].id
        db_item = models.Item(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item














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
