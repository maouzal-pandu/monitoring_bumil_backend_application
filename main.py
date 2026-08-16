from contextlib import asynccontextmanager

from fastapi import FastAPI
from config.database import Base, engine
import models
from routers import auth_router
from routers import kehamilan_router
from core.scheduler import scheduler

# Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(kehamilan_router)
