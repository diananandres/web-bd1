from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from decouple import config

DATA_USER = config('DATA_USER')
DATA_PASSWORD = config('DATA_PASSWORD')
HOST = config('HOST')
PORT = config('DB_PORT')
DATABASE_NAME = config('DATABASE_NAME')

SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://{}:{}@{}:{}/{}'.format(
    DATA_USER,
    DATA_PASSWORD,
    HOST,
    PORT,
    DATABASE_NAME
)

# async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
# async def get_db():
#     async with AsyncSessionLocal() as db:
#         yield db
#         await db.commit()

# async def get_session():
#     async with AsyncSession(async_engine) as session:
#         yield session

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
