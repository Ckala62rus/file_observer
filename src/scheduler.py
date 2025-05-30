import asyncio
import logging.config
import os
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from services import send_email_with_attachment
from utils.configuration import settings
from utils.logger_project import (
    logging_config,
    # customTime,
)

# Загружаем настройки логирования из словаря `logging_config`
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


async def main():
    scheduler = AsyncIOScheduler({'apscheduler.timezone': 'Europe/Moscow'})
    scheduler.add_job(
        send_email_with_attachment,
        "interval",
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

    # scheduler.add_job(
    #     func=send_email_with_attachment,
    #     trigger=CronTrigger.from_crontab("0 8 * * *"),
    #     kwargs={
    #         "sender_email": "scale@scale.ru",  # from
    #         "receiver_email": "admin@forb.it",  # to
    #         "subject": "Письмо с вложением",
    #         "body": "Это письмо с вложением, отправленное с помощью Python.",
    #         "smtp_server": "mail.ogranization.ru",
    #         "smtp_port": 587,
    #         "login": "www@leather.ru",
    #         "password": "123",
    #     },
    # )
    scheduler.start()
    while True:
        await asyncio.sleep(1000)

    # Пример использования функции
    # send_email_with_attachment(
    #     sender_email="scale@leather.ru",  # from
    #     receiver_email="eovchinnikov@fpkinvest.it",  # to
    #     subject="Письмо с вложением",
    #     body="Это письмо с вложением, отправленное с помощью Python.",
    #     # attachment_path="path/to/your/file.txt",
    #     smtp_server="mail.leather.ru",
    #     smtp_port=587,
    #     login="scale@leather.ru",
    #     password="gOuoO577"
    # )


def main2():
    # path_folder = r"//10.5.3.19/Programs/Документация/CRM/Технический дизайн"
    # path_folder = r"\\10.5.3.19\Programs\Документация\CRM\Технический дизайн"
    # path_folder = r"//10.5.3.228/DAXBOT"



    # path_folder = r"\\rk-media\Архив\Отдел информационных технологий\2. Общая\01---kdedov"
    # path_folder = r"\\10.5.3.48"
    path_folder = r"//10.5.3.48"

    obj = os.scandir(path_folder)

    a = os.walk(path_folder)

    for subdir, dirs, files in os.walk(path_folder):
        logger.info(dirs)
        for file in files:
            print(file)

    logger.info("*****************************")

if __name__ == '__main__':
    # Execution will dirs here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.run(main())
        # main2()
    except (KeyboardInterrupt, SystemExit):
        logger.debug("Application was closed")
