import logging.config
import os

from utils.configuration import settings
from utils.logger_project import logging_config


logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


def get_files() -> dict[str,str]:
    logger.info("Starting file observer")
    out: str = ""
    files_dict:dict[str,str] = {}

    if settings.FILES_PATH is None:
        logger.error("Files path not set in env. file!!!")
        raise Exception("Files path not set in env. file!!")

    for dirpath, _, filenames in os.walk(fr"{settings.FILES_PATH}"):
        for filename in filenames:
            file_path = os.path.abspath(os.path.join(dirpath, filename))
            out +=f"path: {file_path} | file: {filename}"
            files_dict[filename] = file_path

    return files_dict
