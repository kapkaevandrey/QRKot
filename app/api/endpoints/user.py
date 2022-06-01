from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth']
)

router.include_router(
    fastapi_users.get_register_router(),
    prefix='/auth',
    tags=['auth']
)

router.include_router(
    fastapi_users.get_users_router(),
    prefix='/users',
    tags=['users']
)


@router.delete('/users/{id}', tags=['users'], deprecated=True)
def delete_user(id: str):
    """
    You don't need to delete users,
    just set the value of the is_active field to False.
    """
    raise HTTPException(
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail="Deleting users is forbidden"
    )
