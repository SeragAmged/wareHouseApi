from fastapi import FastAPI
from api.routes import router
from api.branch.branch_routes import branch_router
from api.employee.employee_routes import employee_router
from api.item.item_routes import item_router
from api.item_detail.item_detail_routes import item_details_router
from api.check_in_out_book.check_book_routes import check_book_router
from utils.database import engine
from utils.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
app.include_router(branch_router)
app.include_router(item_router)
app.include_router(employee_router)
app.include_router(item_details_router)
app.include_router(check_book_router)
