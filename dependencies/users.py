from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from repositories.users_repository import UsersRepository
from services.users_service import UsersService


def get_users_repository(db: Session = Depends(get_db)):
    return UsersRepository(db)


def get_users_service(
    repo: UsersRepository = Depends(get_users_repository)
):
    return UsersService(repo)
