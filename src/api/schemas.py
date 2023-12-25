from typing import List, Optional
from datetime import date, time
from pydantic import BaseModel
from utils.models import CommentTypesEnum, StatusEnum, OperationTypesEnum

default_item_detail_image: str = "https://demofree.sirv.com/nope-not-here.jpg"
default_pdf: str = "No pdf!"


class TokenBase(BaseModel):
    access_token: str
    token_type: str


class Token(TokenBase):
    employee: "Employee"


class BranchBase(BaseModel):
    name: str


class BranchCreate(BranchBase):
    pass


class Branch(BranchBase):
    id: int
    employees: List["Employee"] = []
    items: List["Item"] = []

    class Config:
        from_attributes = True


class EmployeeBase(BaseModel):
    sesa_id: int
    branch_id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    role: str = "user"


class EmployeeCreate(EmployeeBase):
    password: str


class Employee(EmployeeBase):
    id: int
    branch: "BranchBase"
    comments: List["Comment"] = []
    check_outs: List["CheckOut"] = []
    check_ins: List["CheckIn"] = []
    books: List["Book"] = []
    add_item_detail_records: List["ItemDetailRecord"] = []
    add_item_records: List["ItemRecord"] = []

    class Config:
        from_attributes = True


class EmployeeSecret(Employee):
    hashed_password: str


class ItemDetailBase(BaseModel):
    name: str
    image_link: str
    category: Optional[str]
    details: Optional[str]

    data_sheet_link: Optional[str] = default_pdf


class ItemDetailCreate(ItemDetailBase):
    pass


class ItemDetail(ItemDetailBase):
    id: int
    quantity: int
    items: List["Item"] = []

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    se_id: int
    item_detail_id: int
    branch_id: int
    serial_number: int
    calibratable: bool
    calibration_date: Optional[date]
    out_of_calibration: Optional[bool]
    calibration_certificate_link: Optional[str]
    status: StatusEnum = StatusEnum.available


class ItemCreate(ItemBase):
    item_detail_name: str
    branch_name: str
    employee_sesa_id: int


class Item(ItemBase):
    id: int
    detail: ItemDetail
    branch: Branch

    booked: bool = False
    comments: List["Comment"] = []
    check_outs: List["CheckOut"] = []
    check_ins: List["CheckIn"] = []
    book: Optional["Book"]
    add_item_record: List["ItemRecord"] = []

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    employee_id: int
    item_id: int
    comment: str
    date: date
    time: time
    type: CommentTypesEnum = CommentTypesEnum.normal


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    item: Item
    employee: "Employee"

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
    work_order: Optional[int]
    jop_name: Optional[str]
    company_lended: Optional[str]
    estimated_Check_in_Date: Optional[date]
    date: date
    time: time


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
    date: date
    time: time


class CheckInCreate(CheckInBase):
    pass


class CheckIn(CheckInBase):
    id: int
    item: Item
    employee: Employee

    class Config:
        from_attributes = True


class ItemDetailRecordBase(BaseModel):
    employee_id: int
    item_detail_id: int
    date: date
    time: time
    type: OperationTypesEnum


class ItemDetailRecordCreate(ItemDetailRecordBase):
    pass


class ItemDetailRecord(ItemDetailRecordBase):
    id: int
    item_detail: ItemDetail
    employee: Employee

    class Config:
        from_attributes = True


class ItemRecordBase(BaseModel):
    employee_id: int
    item_id: int
    operation_type: OperationTypesEnum
    

class ItemRecordCreate(ItemRecordBase):
    pass

class ItemRecord(ItemRecordBase):
    id: int
    item: Item
    employee: Employee
    date: date
    time: time

    class Config:
        orm_mode = True