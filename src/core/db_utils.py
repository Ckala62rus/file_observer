from sqlalchemy import text

from core.db import async_session
from domains.models import create_tables


async def init_db():

    # Check db connection
    async with async_session() as session:
        # Perform database operations here using 'session'

        # Example: Executing a query
        result = await session.execute(text("SELECT 1"))
        print(result.scalar())

        await session.commit()  # Commit changes if needed

    # Create tables
    await create_tables()
