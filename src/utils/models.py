from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Time, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from datetime import datetime, timezone
import enum
from utils.database import Base


class StatusEnum(str, enum.Enum):
    available = "available"
    out_of_service = "out of service"
    job_assigned = "job assigned"
    booked = "booked"
    lended = "lended"
    messing_item = "messing item"
    out_of_calibration = "out of calibration"
    calibration_due = "calibration due"
    test_and_tag_due = "test and tag due"


class CommentsEnum(str, enum.Enum):
    needs_action = "needs_action"
    normal = "normal"


class Branch(Base):
    __tablename__ = "branch"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), index=True, unique=True, nullable=False)

    has = relationship("Employee", back_populates="works")
    items = relationship("Item", back_populates="branch_owner")


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True,
                autoincrement=True, index=True)
    branch_id = Column(Integer, ForeignKey(Branch.id), nullable=False)

    sesa_id = Column(Integer, unique=True, index=True,
                     nullable=False)
    first_name = Column(String(255), index=True, nullable=False)
    last_name = Column(String(255), index=True, nullable=False)
    email = Column(String(255),  unique=True, index=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)
    phone = Column(String(26), unique=True, nullable=True)

    role = Column(String(255), default="SR", nullable=False)

    works_at = relationship("Branch", back_populates="has")

    comments = relationship("Comment", back_populates="employee")
    check_out = relationship("CheckOut", back_populates="employee")
    check_in = relationship("CheckIn", back_populates="employee")
    book = relationship("Book", back_populates="employee")

    add_item_detail_record = relationship(
        "AddItemDetailRecord", back_populates="employee")
    add_item_record = relationship("AddItemRecord", back_populates="employee")


class ItemDetail(Base):
    __tablename__ = "itemDetail"

    id = Column(Integer, primary_key=True,  autoincrement=True, index=True)
    name = Column(String(255), index=True, nullable=False, unique=True)
    image_link = Column(
        String(2083), default="https://demofree.sirv.com/nope-not-here.jpg", nullable=False)
    category = Column(String(255), nullable=True)
    details = Column(String(255), nullable=True)
    quantity = Column(Integer, default=0, nullable=False)
    data_sheet_link = Column(String(2083), default="No pdf!", nullable=True)

    items = relationship("Item", back_populates="details")
    has_item_detail_record = relationship(
        "AddItemDetailRecord", back_populates="item")


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True,  autoincrement=True, index=True)
    item_detail_id = Column(Integer, ForeignKey(ItemDetail.id), nullable=False)
    branch_id = Column(Integer, ForeignKey(Branch.id), nullable=False)

    se_id = Column(Integer, unique=True, index=True, nullable=False)
    serial_number = Column(Integer, unique=True, nullable=False)

    calibratable = Column(Boolean, nullable=False)
    calibration_date = Column(Date, nullable=True)
    out_of_calibration = Column(
        Boolean, default=False, nullable=True)
    calibration_certificate_link = Column(String(2083), nullable=True)

    status = Column(Enum(StatusEnum),
                    default=StatusEnum.available, nullable=False)

    work_order = Column(Integer, nullable=True)
    jop_name = Column(String(255), nullable=True)

    company_lended = Column(String(255), nullable=True)
    booked = Column(Boolean, default=False, nullable=False)

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

    comment = Column(String(400), nullable=False)
    date = Column(Date, default=datetime.now(
        timezone.utc).date(), nullable=False)
    time = Column(Time, default=datetime.now(
        timezone.utc).time(), nullable=False)
    type = Column(Enum(CommentsEnum),
                  default=CommentsEnum.normal, nullable=False)

    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    item_id = Column(Integer, ForeignKey(Item.id), index=True, nullable=False)

    item = relationship("Item", back_populates="comments")
    employee = relationship("Employee", back_populates="comments")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True,  autoincrement=True, index=True)
    item_id = Column(Integer, ForeignKey(Item.id), index=True, nullable=False)
    employee_id = Column(Integer, ForeignKey(
        Employee.id), index=True, nullable=False)
    future_check_out_date = Column(Date, nullable=True)
    booked_for_work_order = Column(Integer, nullable=False)
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
                  default=datetime.now(timezone.utc).date(), nullable=False)
    time = Column(Time, index=True,
                  default=datetime.now(timezone.utc).time(), nullable=False)

    estimated_Check_in_Date = Column(Date, nullable=True)

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
                  default=datetime.now(timezone.utc).date(), nullable=False)
    time = Column(Time, index=True,
                  default=datetime.now(timezone.utc).time(), nullable=False)

    item = relationship("Item", back_populates="check_in")
    employee = relationship("Employee", back_populates="check_in")


class AddItemDetailRecord(Base):
    __tablename__ = "addItemDetailRecord"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey(
        Employee.id), index=True, nullable=False)
    tool_id = Column(Integer, ForeignKey(Item.id), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    item = relationship("Item", back_populates="add_item_detail_record")
    employee = relationship(
        "Employee", back_populates="add_item_detail_record")


class AddItemRecord(Base):
    __tablename__ = "addItemRecord"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey(
        Employee.id), index=True, nullable=False)
    item_id = Column(Integer, ForeignKey(Item.id), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    item = relationship("Item", back_populates="add_item_record")
    employee = relationship("Employee", back_populates="add_item_record")
