import asyncio
import logging.config

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from services import send_email_with_attachment
from utils.configuration import settings
from utils.logger_project import (
    logging_config,
)

# Загружаем настройки логирования из словаря `logging_config`
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


async def main():
    scheduler = AsyncIOScheduler({'apscheduler.timezone': 'Europe/Moscow'})
    scheduler.add_job(
        send_email_with_attachment,
        # trigger="interval",
        trigger=CronTrigger.from_crontab("0 8 * * *"),
        seconds=5,
        max_instances=1,
        kwargs={
            "sender_email": settings.SENDER_EMAIL,  # from
            "receiver_email": settings.RECEIVER_EMAIL,  # to
            "subject": "Письмо с вложением",
            "body": "Это письмо с вложением, отправленное с помощью Python.",
            "smtp_server": settings.SMTP_SERVER,
            "smtp_port": 587,
            "login": settings.EMAIL_LOGIN,
            "password": settings.EMAIL_PASSWORD,
        },
    )

    scheduler.start()
    while True:
        await asyncio.sleep(1000)


if __name__ == '__main__':
    # Execution will dirs here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.debug("Application was closed")
