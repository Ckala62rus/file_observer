import logging.config
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# from src.utils.logger_project import logging_config
from utils.logger_project import logging_config

# Загружаем настройки логирования из словаря `logging_config`
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


def send_email_with_attachment(
        sender_email: str,
        receiver_email: str,
        subject: str,
        body: str,
        smtp_server: str,
        smtp_port: int,
        login: str,
        password: str,
        attachment_path: str = None,
):
    """
    Метод для отправки писем с возможностью прикрепления файла

    :param sender_email:
    :param receiver_email:
    :param subject:
    :param body:
    :param attachment_path:
    :param smtp_server:
    :param smtp_port:
    :param login:
    :param password:
    :return:
    """
    logger.info("***** Send email start *****")

    path_folder = r"//10.5.3.19/Programs/Документация/CRM/Технический дизайн"
    # path_folder = r"\\10.5.3.19\Programs\Документация\CRM\Технический дизайн"
    # path_folder = r"//10.5.3.228/DAXBOT"
    # path_folder = r"\\rk-media\Архив\Отдел информационных технологий\2. Общая\01---kdedov"
    # path_folder = r"\\10.5.3.48\Архив\Отдел информационных технологий\2. Общая\01---kdedov"

    obj = os.scandir(path_folder)

    a = os.walk(path_folder)

    for subdir, dirs, files in os.walk(path_folder):
        logger.info(dirs)
        for file in files:
            print(file)


    # Создаем объект MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    logger.info("Send message ... ")

    # Добавляем тело письма
    msg.attach(MIMEText(body, 'plain'))

    # Добавляем файл
    # attach_perform(attachment_path, msg)

    # Устанавливаем соединение с сервером
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(login, password)

    # Отправляем письмо
    # server.sendmail(sender_email, receiver_email, msg.as_string())
    # server.quit()
    logger.info("Send message ... ")

    logger.info("***** Send email finished ***** \n")


def attach_perform(
        attachment_path: str,
        msg: MIMEMultipart
):
    """
    Attachment file
    :param msg:
    :param attachment_path:
    :return:
    """
    # Открываем файл для чтения в бинарном режиме
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Кодируем файл в base64
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachment_path}",
    )

    # Добавляем вложение к нашему сообщению
    msg.attach(part)
