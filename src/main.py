from fastapi import FastAPI
from api.branch import routes as BranchRouter
from api.routes import router as Router

from utils.database import engine
from utils.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(Router)
app.include_router(BranchRouter.router)
