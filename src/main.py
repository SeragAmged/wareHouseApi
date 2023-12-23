from fastapi import FastAPI
from api.routes import router
from api.branch import routs
from utils.database import engine
from utils.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
app.include_router(routs.branch_router)
