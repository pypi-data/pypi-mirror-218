import os
import requests
import smtplib
from email.mime.text import MIMEText
import logging
from logging.handlers import RotatingFileHandler

import tdsl
from tdsl import *
from tdsl import dinj

print('notify module loaded')


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
os.makedirs('log', exist_ok=True)
fh = RotatingFileHandler(os.path.join('log', __name__ + '.log'), mode='a', maxBytes=1024 * 5, backupCount=0)
fh.setLevel(logging.DEBUG)
frmttr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmttr)
log.addHandler(fh)



runtime = dinj.Runtime()


def send_simple_message(from_name, to_addrs, subject, msg):
    print(from_name+runtime.CONFIG.Resources.Notify.Domain)
    return requests.post(
        f"https://api.mailgun.net/v3/{runtime.CONFIG.Resources.Notify.Domain}/messages",
        auth=("api", runtime.CONFIG.Resources.Notify.API_Key),
        data={"from": f'{from_name}@{runtime.CONFIG.Resources.Notify.Domain}',
              "to": to_addrs,
              "subject": subject,
              "text": msg})



def send_smtp_message(from_name, to_addr, subject, msg):

    msg = MIMEText('TML/ETF Notification')
    msg['Subject'] = subject
    msg['From']    = f'{from_name}@{runtime.CONFIG.Resources.Notify.Domain}'
    msg['To']      = to_addr

    s = smtplib.SMTP('smtp.mailgun.org', 587)

    s.login(f'postmaster@{runtime.CONFIG.Resources.Notify.Domain}', runtime.CONFIG.Resources.Notify.SMTP_Password)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

    return 'Sent SMTP Message'