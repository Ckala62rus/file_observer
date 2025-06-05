from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession


# Create an asynchronous engine
engine = create_async_engine("sqlite+aiosqlite:///./database.db")

# Create async session factory
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Define the base for declarative models
Base = declarative_base()
