from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from src.database import Base, engine
from src.routers import router
from src.schemas import DepartmentInfo


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     Base.metadata.create_all(engine)
#     yield
#     Base.metadata.drop_all(engine)


app = FastAPI()
app.include_router(router)