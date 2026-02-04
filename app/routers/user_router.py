from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.services.user_service import UserService
from app.services.dependencies import get_user_service
from app.core.db_session import get_db

router = APIRouter()

@router.post("/users")
def create_user(
    user: User,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.create_user(db, user)
