from fastapi import APIRouter, HTTPException, status, Depends

from database import User
from schemas import SUserAdd, SUser, Token, SUserLogin
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


@router.post("/token")
async def get_token(form_data: SUserLogin = Depends()) -> Token:
    user = await authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(user.email)})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
async def get_me(user_data: SUser = Depends(get_current_user)):
    return SUser.model_validate(user_data)
