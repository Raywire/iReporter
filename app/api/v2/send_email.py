import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email_address = os.getenv('MAIL_USERNAME')
email_password = os.getenv('MAIL_PASSWORD')


def send(receiver, subject, body):
    sender = email_address
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject

    body = body
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, email_password)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
        return True
    except:
        return False
