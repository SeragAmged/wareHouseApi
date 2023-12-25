from fastapi import FastAPI
from api.routes import router
from api.branch.routes import branch_router
from api.employee.routes import employee_router
from api.item.routes import item_router
from utils.database import engine
from utils.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
app.include_router(branch_router)
app.include_router(item_router)
app.include_router(employee_router)
