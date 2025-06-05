import logging
import os
from functools import lru_cache

from dotenv import (
    load_dotenv,
    find_dotenv
)

from utils.path_conf import BasePath

# default file name for find '.env'
load_dotenv(find_dotenv(BasePath.joinpath('.env')))
logger = logging.getLogger(__name__)


class Settings:
    EMAIL_LOGIN: str = os.getenv('EMAIL_LOGIN')
    EMAIL_PASSWORD: str = os.getenv('EMAIL_PASSWORD')
    EMAIL_SMTP: int = os.getenv('EMAIL_SMTP', 587)
    SMTP_SERVER: str = os.getenv('SMTP_SERVER')
    SENDER_EMAIL: str = os.getenv('SENDER_EMAIL')
    RECEIVER_EMAIL: str = os.getenv('RECEIVER_EMAIL')

    FILES_PATH: str = os.getenv('FILES_PATH')

    # Database
    SQLALCHEMY_DATABASE_URL: str = f"sqlite:///database.db"

    # Email for send report
    EMAILS: list = os.getenv('EMAILS')


# Декоратор lru_cache для хэширования конфига, что бы при следующих обращениях брался его кеш
@lru_cache
def _get_settings() -> Settings:
    """
    Load settings from env
    :return:
    """
    return Settings()


# Создание экземпляра конфигурационного класса
settings = _get_settings()
