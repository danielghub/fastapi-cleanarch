from fastapi import FastAPI
from app.routers import user_router
from app.core.database import Base, engine
from app.models import user_entity

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clean FastAPI Project")

app.include_router(user_router.router)

@app.get("/")
def root():
    return {"message": "Clean architecture FastAPI 🚀"}
