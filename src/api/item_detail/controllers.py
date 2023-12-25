from typing import List
from sqlalchemy.orm import Session
from utils import models
from api import schemas

def add_item_details(db:Session,item_details:schemas.ItemDetailCreate) -> models.ItemDetail | None:
    db_item_details = models.ItemDetail(**item_details.model_dump())
    db.add(db_item_details)
    db.commit()
    db.refresh(db_item_details)
    return db_item_details

def get_item_details(db:Session,skip: int = 0, limit: int = 100) -> list[models.ItemDetail]:
    return db.query(models.ItemDetail).order_by(models.ItemDetail.name).offset(skip).limit(limit).all()

def get_item_detail_by_id(db: Session, id: int) -> models.ItemDetail | None:
    return db.query(models.ItemDetail).filter(models.ItemDetail.id == id).first()


def get_item_details_by_name(db:Session,name:str) -> models.ItemDetail | None:
    return db.query(models.ItemDetail).filter(models.ItemDetail.name == name).first()



#TODO:
# add itemDetail
# also add records for it with type from the enums

# delete itemDetail
# also add records for it with type from the enums

# update itemDetail
# also add records for it with type from the enums

# get itemdetail by name
# get itemdetail by id


# Get CURRENT available items

#TODO:add quantity trigger for inserting