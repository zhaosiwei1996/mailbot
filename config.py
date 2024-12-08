import logging
import os
import platform

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s [%(funcName)s]-%(process)d %(message)s')
logger = logging.getLogger(__name__)

if platform.system().lower() == 'windows':
    mysqlurl = "mysql://root:111111@localhost:3306/mailbot"
    uvicorn_debug = True
    uvicorn_host = "localhost"
    uvicorn_port = 8000
    uvicorn_reload = True
    # oss
    aws_endpoint = 'http://localhost:9000'
    access_key = 'minioadmin'
    secret_key = 'minioadmin'
    bucket_name = 'email-attachment-file'
    local_file_path = './tmp/'

    # email
    mail_user = "no-reply@aizhao.pro"
    mail_password = "tfMrFVxaP3U64tab8sPa"
    mail_from = "no-reply@aizhao.pro"
    mail_server = "smtp.qiye.aliyun.com"
    mail_port = 465
    mail_ssl = True
    mail_tls = False
    send_sleep_time = 10
elif platform.system().lower() == 'linux':
    mysqlurl = os.environ.get('DB_URL')
    uvicorn_host = os.environ.get('UVICRON_HOST')
    uvicorn_port = int(os.environ.get('UVICRON_PORT'))
    uvicorn_reload = False
    if os.environ.get('UVICRON_DEBUG') == 'on':
        uvicorn_debug = True
    else:
        uvicorn_debug = False
    # oss
    aws_endpoint = os.environ.get('AWS_ENDPOINT')
    access_key = os.environ.get('AWS_ACCESS_KEY')
    secret_key = os.environ.get('AWS_SECRET_KEY')
    bucket_name = os.environ.get('AWS_BUCKET_NAME')
    local_file_path = './tmp/'

    # email
    mail_user = os.environ.get('MAIL_USER')
    mail_password = os.environ.get('MAIL_PASSWORD')
    mail_from = os.environ.get('MAIL_FROM')
    mail_server = os.environ.get('MAIL_SERVER')
    mail_port = int(os.environ.get('MAIL_PORT'))
    mail_ssl = True
    mail_tls = False
    send_sleep_time = int(os.environ.get('MAIL_SEND_SLEEP_TIME'))
