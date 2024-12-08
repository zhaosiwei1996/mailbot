from fastapi import APIRouter, Request, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from libs.models import *
from libs.utils import *
import logging
import boto3
import os
import asyncio
import config

router = APIRouter()

s3_client = boto3.client('s3', endpoint_url=config.aws_endpoint,
                         aws_access_key_id=config.access_key,
                         aws_secret_access_key=config.secret_key)

mailconf = ConnectionConfig(MAIL_USERNAME=config.mail_user, MAIL_PASSWORD=config.mail_password,
                            MAIL_PORT=config.mail_port, MAIL_SERVER=config.mail_server,
                            MAIL_SSL_TLS=config.mail_ssl, MAIL_FROM=config.mail_from, MAIL_STARTTLS=config.mail_tls)


async def send_mail(sendmailid, recipients, title, text, attachments):
    try:
        # 下载附件
        attachment_paths = []
        for attachment in attachments:
            local_path = os.path.join(config.local_file_path, attachment['originalFilename'])
            await asyncio.to_thread(
                s3_client.download_file,
                config.bucket_name,
                attachment['filename'],
                local_path
            )
            attachment_paths.append(local_path)

        # 然后开始循环多收件人发送邮件
        for mailaddress in recipients.split(","):
            message = MessageSchema(
                subject=title,
                recipients=[mailaddress],
                body=text,
                subtype="html",
                attachments=attachment_paths
            )
            fm = FastMail(mailconf)
            await fm.send_message(message)
            # 等待10秒发送下一个
            await asyncio.sleep(config.send_sleep_time)
    except Exception as e:
        logging.error(f"Error: {e}")
        await t_send_mail_history.filter(id=sendmailid.id).update(email_send_status=e)
        raise HTTPException(status_code=500,
                            detail=str(BaseUtils.send_default_info(500, BaseUtils.get_client_ip(), "/api/mail/send",
                                                                   e)))
    else:
        await t_send_mail_history.filter(id=sendmailid.id).update(email_send_status="success")
        return HTTPException(status_code=200,
                             detail=str(BaseUtils.send_default_info(200, BaseUtils.get_client_ip(), "/api/mail/send",
                                                                    "Emails sent successfully!")))


@router.post("/api/mail/send")
async def send_mail_api(request: Request):
    try:
        data = await request.json()
        logging.debug(data)
        recipients = data.get("recipients")
        title = data.get("title")
        text = data.get("text")
        attachments = data.get("attachments", [])
        # 先插入邮件发送数据
        await t_send_mail_history.create(email_recipients=recipients, email_title=title, email_text=text,
                                         email_send_status="no send", client_ip_address=BaseUtils.get_client_ip())
        # 获取邮件发送数据id
        sendmailid = await t_send_mail_history.filter(email_title=title).order_by('-create_time').first()

        for attachmentslist in attachments:
            # 再插入附件表
            await t_send_mail_attachments.create(t_send_mail_history_id=sendmailid.id,
                                                 filename_md5=attachmentslist['filename'], original_filename=
                                                 attachmentslist['originalFilename'])

    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500,
                            detail=str(BaseUtils.send_default_info(500, BaseUtils.get_client_ip(), "/api/mail/send",
                                                                   e)))
    else:
        return await send_mail(sendmailid, recipients, title, text, attachments)
