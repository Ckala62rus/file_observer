import logging.config
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from utils.logger_project import logging_config
from utils.configuration import settings

# Загружаем настройки логирования из словаря `logging_config`
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


def send_email_with_attachment(
        receiver_email: str,
        subject: str,
        body: str,
        # smtp_server: str,
        # smtp_port: int,
        # login: str,
        # password: str,
        attachment_path: str = None,
):
    """
    Метод для отправки писем с возможностью прикрепления файла

    :param receiver_email:
    :param subject:
    :param body:
    :param attachment_path:
    :return:
    """
    logger.info("***** Send email start *****")

    sender_email: str = settings.EMAIL_LOGIN
    smtp_server: str = settings.SMTP_SERVER
    smtp_port: int = settings.EMAIL_SMTP
    login: str = settings.EMAIL_LOGIN
    password: str = settings.EMAIL_PASSWORD

    # Создаем объект MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    logger.info("Send message ... ")

    # Добавляем тело письма
    msg.attach(MIMEText(body, 'plain'))
    # msg.attach(MIMEText(res, 'plain'))

    # Добавляем файл
    # attach_perform(attachment_path, msg)

    # Создание безопасного контекста SSL
    context = ssl.create_default_context()

    # Устанавливаем соединение с сервером
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()  # Может быть опущен
        server.starttls(context=context) # Безопасное соединение
        server.ehlo()  # Может быть опущен
        server.login(login, password)

        # Код отправки письма
        # Отправляем письмо
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        logger.info("Send message ... ")

    except Exception as e:
        # Выводим текст ошибки в stdout
        logger.info(e)
        print(e)
    finally:
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
