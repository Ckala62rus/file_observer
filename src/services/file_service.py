import json
import logging.config

from domains.models import File
from repository.file_repository import create_file, get_file_by_filename
from services import send_email_with_attachment
from utils.configuration import settings
from utils.logger_project import logging_config
from utils.recursive_file_observer import get_files


logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

async def save_file_to_db_and_send_notification() -> None:
    # get all files from folder
    files = get_files()

    # save files to db
    files_model: list[File] = []

    for filename, filepath in files.items():

        # exist file on db or not?
        isExists = await get_file_by_filename(filename)

        if isExists is None:
            file = await create_file(filename, filepath)
            logger.info(f"File was created with id: {file.id} | filename: {file.filename} ")
            files_model.append(file)

    logger.info(f"**** Saved {len(files_model)} files to database")

    if len(files_model) > 0:
        # prepare message for send email
        message = "Документ для подтверждения ресурса размещен \n\n"

        for file_model in files_model:
            message += f"Название файла: {file_model.filename} | Путь до файла: {file_model.path} \n"

        emails = json.loads(settings.EMAILS)
        emails_list = ' | '.join(str(x) for x in emails)

        message += f"Список получателей: {emails_list} \n\n"

        for email in emails:
            send_email_with_attachment(
                receiver_email=email,
                subject="Покрытие заказов на продажу",
                body=message
            )
