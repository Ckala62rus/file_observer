import logging.config

from sqlalchemy import select

from core.db import async_session
from domains.models import File
from utils.logger_project import logging_config


logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

# Define async CRUD operations
async def create_file(file_name: str, path: str) -> File:
    logger.info(f"Creating file_name {file_name} | path {path}")

    async with async_session() as session:
        file = File(filename=file_name, path=path)
        session.add(file)
        await session.commit()
        logger.info(f"File id {file.id} | path {file.filename}")
        return file

async def get_file_by_filename(file_name: str) -> File:
    logger.info(f"get file with file_name {file_name}")
    async with async_session() as session:
        result = await session.execute(select(File).where(File.filename == file_name))
        return result.scalar_one_or_none()
