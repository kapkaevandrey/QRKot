from typing import Union

from fastapi import Depends
from fastapi_users import (
    BaseUserManager, FastAPIUsers, InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import UserTable
from app.schemas.user import User, UserCreate, UserUpdate, UserRead


##############################################################################
# backend configuration                                                      #
##############################################################################
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)


##############################################################################
# User Manager configurations                                                #
##############################################################################
class UserManager(BaseUserManager[UserCreate, UserRead]):
    user_db_model = UserRead
    reset_password_token_secret = settings.secret
    verification_token_secret = settings.secret

    async def validate_password(
            self, password: str, user: Union[UserCreate, UserRead]
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )


##############################################################################
# Depends                                                                    #
##############################################################################
# Я думаю это метод должен быть в файле db.py так имеет отношение к базе данных
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(UserRead, session, UserTable)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

##############################################################################
# User Configuration                                                         #
##############################################################################
fastapi_users = FastAPIUsers(
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
    user_model=User,
    user_db_model=UserRead,
    user_create_model=UserCreate,
    user_update_model=UserUpdate
)

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)