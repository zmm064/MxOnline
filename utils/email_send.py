import string, random

from users.models import EmailVerifyRecord
from django.core.mail import send_mail, EmailMessage
from MxOnline.settings import EMAIL_FROM




def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    random_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))

    # 发送验证码之前先保存相关的记录
    email_record.code = random_str
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == "register":
        email_title = "mtianyan慕课小站 注册激活链接"
        email_body = "欢迎注册mtianyan的慕课小站: 请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/" + random_str
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])