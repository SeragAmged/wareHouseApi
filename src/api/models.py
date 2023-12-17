#!/usr/bin/env python3
from datetime import datetime
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from .database import Base


class Branch(Base):
    __tablename__ = "branch"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    branch_name = Column(String, index=True)

    has = relationship("Employee", back_populates="works")
    items = relationship("Item", back_populates="branch_owner")


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True,
                autoincrement=True, index=True)  # database id

    sesa_id = Column(Integer, unique=True, index=True,
                     nullable=False)  # company id
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String,  unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)

    branch_id = Column(Integer, ForeignKey(Branch.id), nullable=False)

    works_at = relationship("Branch", back_populates="has")
    comments = relationship("Comment", back_populates="employee")

    check_out = relationship("CheckOut", back_populates="employee")
    check_in = relationship("CheckIn", back_populates="employee")

    add_item_detail_record = relationship(
        "AddItemDetailRecord", back_populates="employee")
    add_item_record = relationship("AddItemRecord", back_populates="employee")


class ItemDetail(Base):
    __tablename__ = "itemDetail"

    id = Column(Integer, primary_key=True,  autoincrement=True, index=True)
    name = Column(String, index=True, nullable=False)
    image_link = Column(
        String, default="https://demofree.sirv.com/nope-not-here.jpg")
    category = Column(String)  # TODO:nullable or no?
    details = Column(String)  # TODO:nullable or no?
    quantity = Column(Integer, default=0, nullable=False)
    data_sheet_link = Column(String)

    items = relationship("Item", back_populates="details")
    has_item_detail_record = relationship(
        "ItemDetailsRecord", back_populates="add")


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True,  autoincrement=True, index=True)
    se_id = Column(Integer, unique=True, index=True, nullable=False)
    serial_number = Column(Integer, unique=True, nullable=False)

    calibration_date = Column(Date)
    out_of_calibration = Column(Boolean, default=False, nullable=False)
    calibration_certificate_link = Column(String, nullable=False)

    # TODO: will implement enum for some categories
    status = Column(String, nullable=False)
    # TODO: check WhatsApp details
    work_order = Column(Integer, nullable=True)
    company_lended = Column(String, nullable=True)
    booked = Column(Boolean, default=False, nullable=False)

    item_detail_id = Column(Integer, ForeignKey(ItemDetail.id))
    branch_id = Column(Integer, ForeignKey(Branch.id))

    detail = relationship("ItemDetail", back_populates="items")
    branch_owner = relationship("Branch", back_populates="items")
    comments = relationship("Comment", back_populates="item")

    check_out = relationship("CheckOut", back_populates="item")
    check_in = relationship("CheckIn", back_populates="item")

    add_item_detail_record = relationship(
        "AddItemDetailRecord", back_populates="item")
    add_item_record = relationship("AddItemRecord", back_populates="item")


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True,
                autoincrement=True, index=True)

    comment = Column(String, nullable=False)
    date = Column(Date, default=datetime.now().date(), nullable=False)
    time = Column(Time, default=datetime.now().time(), nullable=False)
    type = Column(String)  # TODO: implement enum types

    employee_id = Column(Integer, ForeignKey(Employee.id))
    item_id = Column(Integer, ForeignKey(Item.id), index=True)

    item = relationship("Item", back_populates="comments")
    employee = relationship("Employee", back_populates="comments")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True,  autoincrement=True, index=True,)
    item_id = Column(Integer, ForeignKey(Item.id), index=True, nullable=False)
    employee_id = Column(Integer, ForeignKey(
        Employee.id), index=True, nullable=False)
    future_check_out_date = Column(Date, nullable=True)

    item = relationship("Item", back_populates="book")
    employee = relationship("Employee", back_populates="book")


class CheckOut(Base):
    __tablename__ = "checkOut"

    id = Column(Integer, primary_key=True,
                index=True, autoincrement=True)

    item_id = Column(Integer, ForeignKey(Item.id), index=True, nullable=False)
    employee_id = Column(Integer, ForeignKey(
        Employee.id), nullable=False)

    date = Column(Date, index=True,
                  default=datetime.now().date(), nullable=False)
    time = Column(Time, index=True,
                  default=datetime.now().time(), nullable=False)

    estimated_Check_in_Date = Column(Date)

    item = relationship("Item", back_populates="check_out")
    employee = relationship("Employee", back_populates="check_out")


class CheckIn(Base):
    __tablename__ = "checkIn"

    id = Column(Integer, primary_key=True,
                index=True, autoincrement=True)

    item_id = Column(Integer, ForeignKey(Item.id), index=True, nullable=False)
    employee_id = Column(Integer, ForeignKey(
        Employee.id), nullable=False)

    date = Column(Date, index=True,
                  default=datetime.now().date(), nullable=False)
    time = Column(Time, index=True,
                  default=datetime.now().time(), nullable=False)

    item = relationship("Item", back_populates="check_in")
    employee = relationship("Employee", back_populates="check_in")


class AddItemDetailRecord(Base):
    __tablename__ = "addItemDetailRecord"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey(Employee.id), index=True)
    tool_id = Column(Integer, ForeignKey(Item.id))
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    item = relationship("Item", back_populates="add_item_detail_record")
    employee = relationship(
        "Employee", back_populates="add_item_detail_record")


class AddItemRecord(Base):
    __tablename__ = "addItemRecord"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey(Employee.id), index=True)
    item_id = Column(Integer, ForeignKey(Item.id))
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    item = relationship("Item", back_populates="add_item_record")
    employee = relationship("Employee", back_populates="add_item_record")
