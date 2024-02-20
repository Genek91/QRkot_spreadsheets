import logging
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate

logging.basicConfig(level=logging.INFO)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < settings.min_len_password:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Пароль не должен содержать адрес электронной почты'
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        logging.info(f'Пользователь {user.email} зарегистрирован.')

    # Вариант быстрого добавления возможности деативироватся пользователям
    # from app.schemas.user import UserUpdate

    # async def update(
    #     self,
    #     user_update: UserUpdate,
    #     user: User,
    #     safe: bool = False,
    #     request: Optional[Request] = None
    # ) -> User:
    #     if user.is_superuser:
    #         safe = False
    #     else:
    #         if user_update.is_active is False:
    #             safe = False
    #             user_update.is_superuser = user.is_superuser
    #             user_update.is_verified = user.is_verified

    #     updated_user = await super().update(user_update, user, safe, request)

    #     return updated_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
