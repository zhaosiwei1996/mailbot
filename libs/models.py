from tortoise import fields
from tortoise.models import Model


# 附件表，存储每个附件的 MD5 和原始文件名
class t_send_mail_attachments(Model):
    id = fields.IntField(pk=True, description="附件ID")
    t_send_mail_history_id = fields.IntField(Fieldmax_length=11, description="关联邮件发送历史记录id")
    filename_md5 = fields.CharField(max_length=200, description="附件 MD5 值")
    original_filename = fields.CharField(max_length=200, description="附件的原始文件名")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "t_send_mail_attachments"  # 附件表
        table_description = "附件表，存储每个附件的 MD5 和原始文件名"


# 邮件发送历史记录表
class t_send_mail_history(Model):
    id = fields.IntField(pk=True, description="邮件任务ID")
    email_recipients = fields.TextField(max_length=200, description="邮件收件人")
    email_title = fields.CharField(max_length=200, description="邮件标题")
    email_text = fields.TextField(description="邮件内容，支持HTML格式")
    email_send_status = fields.TextField(description="邮件发送状态")
    client_ip_address = fields.CharField(max_length=100, description="客户端 IP 地址")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "t_send_mail_history"
        table_description = "邮件发送历史记录表"
