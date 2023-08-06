
from ctypes import Union
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from bbat.date import date_diff
import requests

def send_email(subject="", msg= "", receivers: Union[str, list] = 'meutils@qq.com', _subtype='html', msg_prefix='', msg_suffix='', msg_fn=lambda x: x, date=date_diff(days=0), host2sender=None, **kwargs):
    """
    Args
        subject: 主题
        msg:
        receivers:
        _subtype:
        msg_prefix:
        msg_suffix:
        msg_fn:
        kwargs:
    """

    # init
    # token = get_zk_config("/push/email_token")
    # host, sender = list(token.items())[0]
    if host2sender is None:
        host2sender = {'localhost': 'BOT'}

    host, sender = list(host2sender.items())[0]
    smtp = smtplib.SMTP(host, 25)

    # 主题+内容
    subject = f"👉{subject}📅{date}"

    msg = f"{msg_prefix}{msg_fn(msg)}{msg_suffix}"

    message = MIMEText(msg, _subtype, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = sender

    if isinstance(receivers, str) and receivers.__contains__("@"):
        receivers = [receivers]
    message['To'] = ",".join(receivers)

    try:
        smtp.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(f"{e}: 无法发送邮件")



def send_feishu(title='TEST', text='', hook_url='logger'):
    requests.post(hook_url, json={"title": str(title), "text": f'{text} '})


if __name__ == '__main__':
    send_feishu(hook_url='')

    send_email("测试邮件", msg='邮件内容')
