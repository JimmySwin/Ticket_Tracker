import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, to_email, from_email, app_password):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, app_password)
        server.send_message(msg)

    print(f"✅ Email sent to {to_email}")
    
