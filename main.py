from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables, delete_tables
from routers.user import router as auth_router
from utils import register_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База delete_tables")
    email = 'admin'
    password = 'admin'
    admin = await register_admin(email, password)
    print(f"Cоздан админ {admin.email}/{password}")
    yield
    await delete_tables()
    print("База очищена")

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
