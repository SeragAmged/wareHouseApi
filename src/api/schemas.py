#!/usr/bin/env python3
from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel, EmailStr

#Unsupported escape sequence in string literal: Ignore
"""

  ______     ___       __    __  .___________.     _______ .______   .___________.     ______   ______    _______   _______ 
 /      |   /   \     |  |  |  | |           |    /  _____||   _  \  |           |    /      | /  __  \  |       \ |   ____|
|  ,----'  /  ^  \    |  |__|  | `---|  |----`   |  |  __  |  |_)  | `---|  |----`   |  ,----'|  |  |  | |  .--.  ||  |__   
|  |      /  /_\  \   |   __   |     |  |        |  | |_ | |   ___/      |  |        |  |     |  |  |  | |  |  |  ||   __|  
|  `----./  _____  \  |  |  |  |     |  |        |  |__| | |  |          |  |        |  `----.|  `--'  | |  '--'  ||  |____ 
 \______/__/     \__\ |__|  |__|     |__|         \______| | _|          |__|         \______| \______/  |_______/ |_______|
                                                                                                                            

"""
"""
code not reviewed yet I want to sleep

#TODO:check nullability and check enums yet

"""

class BranchSchema(BaseModel):
    id: int
    branch_name: str


class EmployeeSchema(BaseModel):
    id: int
    sesa_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    role: str
    branch_id: int


class ItemDetailSchema(BaseModel):
    id: int
    name: str
    image_link: str
    category: Optional[str]
    details: Optional[str]
    quantity: int
    data_sheet_link: Optional[str]


class ItemSchema(BaseModel):
    id: int
    se_id: int
    serial_number: int
    calibration_date: Optional[date]
    out_of_calibration: bool
    calibration_certificate_link: str
    status: str
    work_order: Optional[int]
    company_lended: Optional[str]
    booked: bool
    item_detail_id: Optional[int]
    branch_id: Optional[int]


class CommentSchema(BaseModel):
    id: int
    comment: str
    date: date
    time: time
    type: Optional[str]
    employee_id: int
    item_id: Optional[int]


class BookSchema(BaseModel):
    id: int
    item_id: int
    employee_id: int
    future_check_out_date: Optional[date]


class CheckOutSchema(BaseModel):
    id: int
    item_id: int
    employee_id: int
    estimated_Check_in_Date: Optional[date]
    date: date
    time: time


class CheckInSchema(BaseModel):
    id: int
    item_id: int
    employee_id: int
    date: date
    time: time


class AddItemDetailRecordSchema(BaseModel):
    id: int
    employee_id: int
    tool_id: int
    date: date
    time: time


class AddItemRecordSchema(BaseModel):
    id: int
    employee_id: int
    item_id: int
    date: date
    time: time
