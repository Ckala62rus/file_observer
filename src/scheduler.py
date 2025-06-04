import asyncio
import logging.config

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from database.db import create_db
from services import send_email_with_attachment
from utils.configuration import settings
from utils.logger_project import (
    logging_config,
)
from utils.recursive_file_observer import get_files

# Загружаем настройки логирования из словаря `logging_config`
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


async def main():
    create_db()

    logger.exception(f"""
            settings.SENDER_EMAIL: {settings.SENDER_EMAIL}
            settings.RECEIVER_EMAIL: {settings.RECEIVER_EMAIL}
        """)

    scheduler = AsyncIOScheduler({'apscheduler.timezone': 'Europe/Moscow'})

    # scheduler.add_job(
    #     send_email_with_attachment,
    #     trigger=CronTrigger.from_crontab("0 8 * * *"),
    #     max_instances=1,
    #     kwargs={
    #         "sender_email": settings.SENDER_EMAIL,  # from
    #         "receiver_email": settings.RECEIVER_EMAIL,  # to
    #         "subject": "Письмо с вложением",
    #         "body": "Это письмо с вложением, отправленное с помощью Python.",
    #         "smtp_server": settings.SMTP_SERVER,
    #         "smtp_port": 587,
    #         "login": settings.EMAIL_LOGIN,
    #         "password": settings.EMAIL_PASSWORD,
    #     },
    # )

    # try:
    #     scheduler.add_job(
    #         send_email_with_attachment,
    #         CronTrigger.from_crontab('* * * * *'),
    #         kwargs={
    #             "sender_email": settings.SENDER_EMAIL,  # from
    #             "receiver_email": settings.RECEIVER_EMAIL,  # to
    #             "subject": "Письмо с вложением",
    #             "body": "Это письмо с вложением, отправленное с помощью Python.",
    #             "smtp_server": settings.SMTP_SERVER,
    #             "smtp_port": 587,
    #             "login": settings.EMAIL_LOGIN,
    #             "password": settings.EMAIL_PASSWORD,
    #         },
    #     )
    # except Exception as e:
    #     logger.exception(e)

    try:
        scheduler.add_job(
            func=get_files,
            trigger=IntervalTrigger(seconds=5),
            max_instances=1,
        )
    except Exception as e:
        logger.exception(e)

    # scheduler.add_job(
    #     send_email_with_attachment,
    #     trigger="interval",
    #     seconds=5,
    #     max_instances=1,
    #     kwargs={
    #         "sender_email": settings.SENDER_EMAIL,  # from
    #         "receiver_email": settings.RECEIVER_EMAIL,  # to
    #         "subject": "Письмо с вложением",
    #         "body": "Это письмо с вложением, отправленное с помощью Python.",
    #         "smtp_server": settings.SMTP_SERVER,
    #         "smtp_port": 587,
    #         "login": settings.EMAIL_LOGIN,
    #         "password": settings.EMAIL_PASSWORD,
    #     },
    # )

    scheduler.start()
    while True:
        await asyncio.sleep(1000)


if __name__ == '__main__':
    # Execution will dirs here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.debug("Application was closed")
