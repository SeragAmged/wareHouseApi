from typing import List, Optional
from datetime import date, time, datetime,  timezone
from pydantic import BaseModel
from utils.models import CommentsEnum, StatusEnum

default_item_detail_image: str = "https://demofree.sirv.com/nope-not-here.jpg"
default_pdf: str = "No pdf!"


class BranchBase(BaseModel):
    name: str


class BranchCreate(BranchBase):
    pass


class Branch(BranchBase):
    id: int
    employees: List["Employee"] = []
    items: list["Item"] = []

    class Config:
        from_attributes = True


class EmployeeBase(BaseModel):
    sesa_id: int
    first_name: str
    last_name: str
    email: str
    hashed_password: str
    phone: Optional[str]
    role: str = "SR"
    branch_id: int


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int
    works_at: Branch
    comments: List["Comment"] = []
    check_out: List["CheckOut"] = []
    check_in: List["CheckIn"] = []
    book: List["Book"] = []
    add_item_detail_record: List["AddItemDetailRecord"] = []
    add_item_record: List["AddItemRecord"] = []

    class Config:
        from_attributes = True


class ItemDetailBase(BaseModel):
    name: str
    image_link: str = default_item_detail_image
    category: Optional[str]
    details: Optional[str]
    quantity: int
    data_sheet_link: Optional[str] = default_pdf


class ItemDetailCreate(ItemDetailBase):
    pass


class ItemDetail(ItemDetailBase):
    id: int
    items: List["Item"] = []

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    item_detail_id: int
    branch_id: int
    se_id: int
    serial_number: int
    calibratable: bool
    calibration_date: Optional[date]
    out_of_calibration: Optional[bool]
    calibration_certificate_link: Optional[str]
    status: StatusEnum = StatusEnum.available


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    detail: ItemDetail
    branch_owner: Branch
    work_order: Optional[int]
    jop_name: Optional[str]
    company_lended: Optional[str]
    booked: Optional[bool]
    comments: List["Comment"] = []
    check_out: List["CheckOut"] = []
    check_in: List["CheckIn"] = []
    book: List["Book"] = []
    add_item_detail_record: List["AddItemDetailRecord"] = []
    add_item_record: List["AddItemRecord"] = []

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    employee_id: int
    item_id: int
    comment: str
    date_: date = datetime.now(timezone.utc).date()
    time_: time = datetime.now(timezone.utc).time()
    type: CommentsEnum = CommentsEnum.normal


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    item: Item
    employee: Employee

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    item_id: int
    employee_id: int
    future_check_out_date: Optional[date]
    booked_for_work_order: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    item: Item
    employee: Employee

    class Config:
        from_attributes = True


class CheckOutBase(BaseModel):
    item_id: int
    employee_id: int
    estimated_Check_in_Date: Optional[date]
    date_: date = datetime.now(timezone.utc).date()
    time_: time = datetime.now(timezone.utc).time()


class CheckOutCreate(CheckOutBase):
    pass


class CheckOut(CheckOutBase):
    id: int
    item: Item
    employee: Employee

    class Config:
        from_attributes = True


class CheckInBase(BaseModel):
    item_id: int
    employee_id: int
    date_: date = datetime.now(timezone.utc).date()
    time_: time = datetime.now(timezone.utc).time()


class CheckInCreate(CheckInBase):
    pass


class CheckIn(CheckInBase):
    id: int
    item: Item
    employee: Employee

    class Config:
        from_attributes = True


class AddItemDetailRecordBase(BaseModel):
    employee_id: int
    item_id: int
    date_: date = datetime.now(timezone.utc).date()
    time_: time = datetime.now(timezone.utc).time()


class AddItemDetailRecordCreate(AddItemDetailRecordBase):
    pass


class AddItemDetailRecord(AddItemDetailRecordBase):
    id: int
    item: Item
    employee: Employee

    class Config:
        from_attributes = True


class AddItemRecordBase(BaseModel):
    employee_id: int
    item_id: int
    date_: date = datetime.now(timezone.utc).date()
    time_: time = datetime.now(timezone.utc).time()


class AddItemRecordCreate(AddItemRecordBase):
    pass


class AddItemRecord(AddItemRecordBase):
    id: int
    item: Item
    employee: Employee

    class Config:
        from_attributes = True
