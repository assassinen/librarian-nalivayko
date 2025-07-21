from fastapi import APIRouter, HTTPException, status, Depends, Response

from database import User
from schemas import SUserAdd, SUser, Token, SUserLogin, SReaderAdd, SUserSkopes
from utils import get_password_hash, authenticate_user, create_access_token, get_current_user

router = APIRouter(prefix='/user', tags=['Пользователи'])


@router.post("/register")
async def register_user(user_data: SUserAdd = Depends()) -> dict:
    user = await User.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await User.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/add_user")
async def add_user(user_data: SReaderAdd = Depends(),
                     current_user: SUser = Depends(get_current_user)) -> dict:
    if not (current_user.is_librarian or current_user.is_admin):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='Пользователь не может добавлять новых пользователей'
        )
    user = await User.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    await User.add(**user_dict)
    return {'message': f'Пользователь {user_data.email} успешно зарегистрирован'}


@router.patch("/edit_user_scopes")
async def edit_user_scopes(user_data: SUserSkopes = Depends(),
                           current_user: SUser = Depends(get_current_user)) -> dict:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='Пользователь менять права пользователям'
        )
    user = await User.find_one_or_none(email=user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Пользователь {user_data.email} не найден'
        )
    user_dict = {k: v for k, v in user_data.model_dump().items()
                 if k in ('is_librarian', 'is_admin') and v is not None}
    user_dict.update(uuid=user.uuid)
    await User.edit_by_uuid(**user_dict)
    return {'message': f'Права пользователю {user_data.email} успешно изменены'}

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MDQ0Mjk1MX0.iDlNyLUPM3sskN7zmn0iI-m6-hdaB4ZEcz23kyOY3Kc
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhc3Nhc3NpbmVuQHlhLnJ1IiwiZXhwIjoxNzUwNDQ0NjU2fQ.QQ5-mqVfDUCTVuERD1RMS5nGDHV6d7YnQIm817t0ev0
@router.post("/token")
async def get_token(user_data: SUserLogin = Depends()) -> Token:
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(user.email)})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
async def get_me(user_data: SUser = Depends(get_current_user)):
    return SUser.model_validate(user_data)
