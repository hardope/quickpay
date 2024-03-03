from email.mime.multipart import MIMEMultipart
import ssl
import smtplib
from email.mime.text import MIMEText
import json
import os

from quickpay.settings import BASE_DIR

with open(os.path.join(BASE_DIR, "credentials.json")) as config_file:
    data = json.load(config_file)

def send_mail(to, subject, body):
    sender = data["email"]
    recipient = to
    password = data["password"]

    mail = MIMEMultipart('alternative')
    mail["From"] = sender
    mail["To"] = recipient
    mail["Subject"] = subject

    mail.attach(MIMEText(body, 'html'))

    context = ssl.create_default_context()

    try:

        with smtplib.SMTP_SSL(data["email_host"], data["email_port"], context=context) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, recipient, mail.as_string())
    except:
        pass
    