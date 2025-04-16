from sqlalchemy.orm import Session
from src.entities.user import User



class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, user_id: str) -> User | None:
        return self.session.query(User).filter(User.uuid == user_id).first()

    def find_all(self) -> list[User]:
        return self.session.query(User).all()

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user: User) -> User:
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User):
        self.session.delete(user)
        self.session.commit()

    def find_by_name(self, user_name: str) -> User | None:
        return self.session.query(User).filter(User.name == user_name).first()
