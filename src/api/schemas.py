from typing import Any, List, Optional
from datetime import date, datetime, time
from pydantic import BaseModel
from utils.models import CommentTypesEnum, StatusEnum, OperationTypesEnum

default_item_detail_image: str = "https://demofree.sirv.com/nope-not-here.jpg"
default_pdf: str = "No pdf!"


# --------TOKEN-----------#
class TokenBase(BaseModel):
    access_token: str
    token_type: str


class Token(TokenBase):
    employee: "Employee"


# --------BRANCH-----------#

class BranchBase(BaseModel):
    name: str


class BranchCreate(BranchBase):
    pass


class Branch(BranchBase):
    id: int
    # employees: List["Employee"] = []
    # items: List["ItemBase"] = []

    class Config:
        from_attributes = True

# --------EMPLOYEE-----------#


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
    branch_name: str


class Employee(EmployeeBase):
    id: int
    branch: "Branch"
    # comments: List["Comment"] = []
    # check_outs: List["CheckOutBase"] = []
    # check_ins: List["CheckInBase"] = []
    # books: List["BookBase"] = []

    class Config:
        from_attributes = True


class EmployeeSecret(Employee):
    hashed_password: str

# --------ITEM_DETAIL-----------#


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
    # items: List["ItemBase"] = []

    class Config:
        from_attributes = True

# --------ITEM-----------#


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


class Item(ItemBase):
    id: int
    booked: bool = False
    detail: ItemDetailBase
    branch: BranchBase
    # book: Optional["BookBase"]
    # comments: List["CommentBase"] = []
    # check_outs: List["CheckOutBase"] = []
    # check_ins: List["CheckInBase"] = []

    class Config:
        from_attributes = True


# --------COMMENT-----------#

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
    item: "ItemBase"
    employee: "EmployeeBase"

    class Config:
        from_attributes = True

# --------BOOK-----------#


class BookBase(BaseModel):
    item_id: int
    employee_id: int
    future_check_out_date: Optional[date]
    booked_for_work_order: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    # item: Item
    # employee: Employee

    class Config:
        from_attributes = True

# --------CHECK-OUT-----------#


class CheckOutBase(BaseModel):
    item_id: int
    employee_id: int
    work_order: Optional[int]
    jop_name: Optional[str]
    company_lended: Optional[str]
    estimated_Check_in_Date: Optional[date]
    date: Any = datetime.utcnow().date()
    time: Any = datetime.utcnow().time()


class CheckOutCreate(CheckOutBase):
    pass


class CheckOut(CheckOutBase):
    id: int
    item: ItemBase
    employee: EmployeeBase
    returned: bool

    class Config:
        from_attributes = True

# --------CHECK-IN-----------#


class CheckInBase(BaseModel):
    item_id: int
    employee_id: int
    date: Any = datetime.utcnow().date()
    time: Any = datetime.utcnow().time()


class CheckInCreate(CheckInBase):
    pass


class CheckIn(CheckInBase):
    id: int
    item: ItemBase
    employee: EmployeeBase

    class Config:
        from_attributes = True
