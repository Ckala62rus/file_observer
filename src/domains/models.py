# Define a model
import datetime

from sqlalchemy import String, text, Column, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from core.db import Base, engine


# Define a model
class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String, index=True, unique=True)
    path: Mapped[str] = mapped_column(String)

    # created_at: Mapped[datetime.datetime] = mapped_column(
    #     server_default=text("TIMEZONE('utc', now())")
    # )
    # updated_at: Mapped[datetime.datetime] = mapped_column(
    #     server_default=text("TIMEZONE('utc', now())"),
    #     onupdate=datetime.datetime.utcnow()
    # )

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __str__(self):
        return f'Filename: {self.filename} => Path: {self}'


# Async function to create tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)