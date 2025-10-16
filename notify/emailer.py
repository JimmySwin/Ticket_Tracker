from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_notification_events(events):
    """Return a list of events that open or close tomorrow."""
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)
    notifications = []

    for event in events:
        name = event['name']
        open_date = event.get('open_date')
        close_date = event.get('close_date')

        if open_date == tomorrow.isoformat():
            notifications.append(f"🎟️ {name} ballot opens tomorrow ({open_date}).")
        if close_date == tomorrow.isoformat():
            notifications.append(f"⏳ {name} ballot closes tomorrow ({close_date}).")

    return notifications


def send_email_notification(notifications, recipient_email):
    """Send an email listing all notifications."""
    if not notifications:
        print("No notifications to send today.")
        return

    sender_email = "your_email@gmail.com"
    app_password = "your_app_password"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🎫 Event Reminder - Upcoming Ballots"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    html_content = "<h2>Upcoming Events</h2><ul>"
    for n in notifications:
        html_content += f"<li>{n}</li>"
    html_content += "</ul>"

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

    print(f"✅ Sent {len(notifications)} notification(s) to {recipient_email}")