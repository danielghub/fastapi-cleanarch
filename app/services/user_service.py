from sqlalchemy.orm import Session
from app.models.user_entity import UserEntity
from app.models.user_model import User

class UserService:

    def create_user(self, db: Session, user: User):
        entity = UserEntity(
            name=user.name,
            age=user.age
        )

        db.add(entity)
        db.commit()
        db.refresh(entity)

        return {
            "id": entity.id,
            "name": entity.name,
            "age": entity.age
        }
