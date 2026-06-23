from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from app.core.database import db_helper
from app.routers.auth import router as auth_router
from app.routers.roles import router as roles_router
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await db_helper.dispose()


app = FastAPI(title="Auth Service", lifespan=lifespan)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(roles_router, prefix="/roles", tags=["roles"])
app.include_router(users_router, prefix="/users", tags=["users"])
