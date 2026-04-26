import smtplib
from email.mime.text import MIMEText
import environ
env = environ.Env()

def send_email(to_email, subject, body):
    smtp_host = "smtp.gmail.com"
    smtp_port = 587

    username='mokshit.simform@gmail.com'
    password='hvitbjxqrnlkotlm'

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = username
    msg["To"] = to_email

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(username, password)

    server.sendmail(
        username,
        [to_email],
        msg.as_string()
    )

    server.quit()