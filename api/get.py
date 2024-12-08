from fastapi.responses import JSONResponse
from fastapi import APIRouter
from libs.models import *
from libs.utils import *
import logging

router = APIRouter()


# getmail status
@router.get("/api/mail/get")
async def getmail():
    emails = await t_send_mail_history.all().values()
    logging.debug(emails)
    return emails
