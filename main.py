from fastapi import FastAPI
from database import engine,Base
from routers import user_router,record_router

app=FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)
app.include_router(record_router.router)
