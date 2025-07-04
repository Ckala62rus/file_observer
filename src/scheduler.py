import asyncio
import logging.config

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from core.db_utils import init_db
from services.file_service import save_file_to_db_and_send_notification
from utils.configuration import settings
from utils.logger_project import (
    logging_config,
)


# Загружаем настройки логирования из словаря `logging_config`
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


async def main():
    await init_db()

    logger.exception(f"""
            settings.SENDER_EMAIL: {settings.SENDER_EMAIL}
            settings.RECEIVER_EMAIL: {settings.RECEIVER_EMAIL}
            settings.CRON_EXPRESSION: {settings.CRON_EXPRESSION}
            settings.RECEIVER_EMAIL: {settings.EMAILS}
        """)

    scheduler = AsyncIOScheduler({'apscheduler.timezone': 'Europe/Moscow'})

    try:
        scheduler.add_job(
            func=save_file_to_db_and_send_notification,
            trigger=CronTrigger.from_crontab(settings.CRON_EXPRESSION),
        )
    except Exception as e:
        logger.exception(e)

    # try:
    #     scheduler.add_job(
    #         # func=get_files,
    #         func=save_file_to_db_and_send_notification,
    #         trigger=IntervalTrigger(seconds=5),
    #         max_instances=1,
    #     )
    # except Exception as e:
    #     logger.exception(e)

    scheduler.start()
    while True:
        await asyncio.sleep(1000)


if __name__ == '__main__':
    # Execution will dirs here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.debug("Application was closed")
