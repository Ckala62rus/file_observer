import logging.config
import os

from utils.configuration import settings
from utils.logger_project import logging_config


logger = logging.getLogger(__name__)


def get_files():
    logger.info("Starting file observer")
    out: str = ""

    for dirpath, _, filenames in os.walk(fr"{settings.FILES_PATH}"):
        for f in filenames:
            a = os.path.abspath(os.path.join(dirpath, f))
            # print(f"path: {a} | file: {f}")
            logger.debug(f"path: {a} | file: {f} \n")
            out +=f"path: {a} | file: {f}"

    logger.info("***** Starting *****")
    logger.info(f"out: {out}")
    logger.info("***** End *****")
    return out
