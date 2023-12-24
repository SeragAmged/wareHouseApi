from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Time, Enum, func
from sqlalchemy.orm import relationship
import enum
from sqlalchemy.orm import declarative_base

from api import employee
Base = declarative_base()


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


class CommentTypesEnum(str, enum.Enum):
    needs_action = "needs_action"
    normal = "normal"


class OperationTypesEnum(str, enum.Enum):
    create = "create"
    update = "Update"
    delete = "delete"


class RolesEnum(int, enum.Enum):
    user = 0
    admin = 1


class Branch(Base):
    __tablename__ = "branch"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), index=True, unique=True, nullable=False)

    employees = relationship("Employee", back_populates="branch")
    items = relationship("Item", back_populates="branch")


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

    role = Column(Enum(RolesEnum), nullable=False)

    branch = relationship("Branch", back_populates="employees")

    comments = relationship("Comment", back_populates="employee")

    check_outs = relationship("CheckOut", back_populates="employee")

    check_ins = relationship("CheckIn", back_populates="employee")
    books = relationship("Book", back_populates="employee")

    item_detail_records = relationship(
        "ItemDetailRecord", back_populates="employee")
    item_records = relationship("ItemRecord", back_populates="employee")

    tokens = relationship("Token", back_populates="employee")


class Token(Base):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True,  autoincrement=True, index=True)
    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    token = Column(String(255), nullable=False)
    expiry_date = Column(Date, nullable=False)

    employee = relationship("Employee", back_populates="tokens")


class ItemDetail(Base):
    __tablename__ = "itemDetail"

    id = Column(Integer, primary_key=True,  autoincrement=True, index=True)
    name = Column(String(255), index=True, nullable=False, unique=True)
    image_link = Column(
        String(2083), default="https://demofree.sirv.com/nope-not-here.jpg", nullable=False)
    category = Column(String(255), nullable=True)
    details = Column(String(255), nullable=True)
    quantity = Column(Integer, default=0, nullable=False)
    data_sheet_link = Column(String(2083), default="No pdf!")

    items = relationship("Item", back_populates="detail")
    add_item_detail_record = relationship(
        "ItemDetailRecord", back_populates="item_detail")


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

    booked = Column(Boolean, default=False, nullable=False)

    check_outs = relationship("CheckOut", back_populates="item")
    check_ins = relationship("CheckIn", back_populates="item")

    book = relationship("Book", back_populates="items")
    comments = relationship("Comment", back_populates="item")

    detail = relationship("ItemDetail", back_populates="items")
    branch = relationship("Branch", back_populates="items")

    add_item_record = relationship("ItemRecord", back_populates="item")


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True,
                autoincrement=True, index=True)

    comment = Column(String(400), nullable=False)
    date = Column(Date, default=func.current_date(), nullable=False)

    time = Column(Time, default=func.current_time(), nullable=False)
    type = Column(Enum(CommentTypesEnum),
                  default=CommentTypesEnum.normal, nullable=False)

    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    item_id = Column(Integer, ForeignKey(Item.id), index=True, nullable=False)

    employee = relationship("Employee", back_populates="comments")
    item = relationship("Item", back_populates="comments")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True,  autoincrement=True, index=True)
    item_id = Column(Integer, ForeignKey(Item.id), index=True, nullable=False)
    employee_id = Column(Integer, ForeignKey(
        Employee.id), index=True, nullable=False)
    future_check_out_date = Column(Date, nullable=True)
    booked_for_work_order = Column(Integer, nullable=False)

    items = relationship("Item", back_populates="book")
    employee = relationship("Employee", back_populates="books")


class CheckOut(Base):
    __tablename__ = "checkOut"

    id = Column(Integer, primary_key=True,
                index=True, autoincrement=True)

    item_id = Column(Integer, ForeignKey(Item.id), index=True, nullable=False)
    employee_id = Column(Integer, ForeignKey(
        Employee.id), nullable=False)

    date = Column(Date, index=True,
                  default=func.current_date(), nullable=False)
    time = Column(Time, index=True,
                  default=func.current_time(), nullable=False)
    
    work_order = Column(Integer, nullable=True)
    jop_name = Column(String(255), nullable=True)

    company_lended = Column(String(255), nullable=True)

    estimated_Check_in_Date = Column(Date, nullable=True)

    item = relationship("Item", back_populates="check_outs")
    employee = relationship("Employee", back_populates="check_outs")


class CheckIn(Base):
    __tablename__ = "checkIn"

    id = Column(Integer, primary_key=True,
                index=True, autoincrement=True)

    item_id = Column(Integer, ForeignKey(Item.id), index=True, nullable=False)
    employee_id = Column(Integer, ForeignKey(
        Employee.id), nullable=False)

    date = Column(Date, index=True,
                  default=func.current_date(), nullable=False)
    time = Column(Time, index=True,
                  default=func.current_time(), nullable=False)

    item = relationship("Item", back_populates="check_ins")
    employee = relationship("Employee", back_populates="check_ins")


class ItemDetailRecord(Base):
    __tablename__ = "itemDetailRecord"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey(
        Employee.id), index=True, nullable=False)
    item_detail_id = Column(Integer, ForeignKey(ItemDetail.id), nullable=False)

    operation_type = Column(Enum(OperationTypesEnum), nullable=False)

    date = Column(Date, default=func.current_date(), nullable=False)
    time = Column(Time, default=func.current_time(), nullable=False)

    item_detail = relationship(
        "ItemDetail", back_populates="add_item_detail_record")
    employee = relationship(
        "Employee", back_populates="item_detail_records")


class ItemRecord(Base):
    __tablename__ = "itemRecord"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey(
        Employee.id), index=True, nullable=False)
    item_id = Column(Integer, ForeignKey(Item.id), nullable=False)

    operation_type = Column(Enum(OperationTypesEnum), nullable=False)
    date = Column(Date,  default=func.current_date(), nullable=False)
    time = Column(Time, default=func.current_time(), nullable=False)

    item = relationship("Item", back_populates="add_item_record")
    employee = relationship("Employee", back_populates="item_records")
