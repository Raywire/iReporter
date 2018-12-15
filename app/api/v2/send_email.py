import smtplib
import os

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

email_address = os.getenv('MAIL_USERNAME')
email_password = os.getenv('MAIL_PASSWORD')

def send(receiver, incident_type, incident_id, incident_status):
    sender = email_address
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Status Change for {0}".format(incident_type)

    body = "The status of the {0} with id: {1} has changed to {2}".format(
        incident_type, incident_id, incident_status)
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, email_password)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
    except:
        pass
