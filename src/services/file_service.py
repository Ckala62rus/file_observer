import logging.config

from repository.file_repository import create_file, get_file_by_filename
from utils.logger_project import logging_config
from utils.recursive_file_observer import get_files


logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

async def save_file_to_db_and_send_notification():
    # get all files from folder
    files = get_files()

    # save files to db
    files_model: list = []

    for filename, filepath in files.items():

        # exist file on db or not?
        isExists = await get_file_by_filename(filename)

        if isExists is None:
            file = await create_file(filename, filepath)
            logger.info(f"File was created with id: {file.id} | filename: {file.filename} ")
            files_model.append(file)

    logger.info(f"Saved {len(files_model)} files to database")
    logger.info(files_model)
