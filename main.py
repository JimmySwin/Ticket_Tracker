from scr.scraper import get_berlin_marathon_date
from notify.emailer import send_email

if __name__ == "__main__":
    text, date = get_berlin_marathon_date()

    subject = "🎟️ Berlin Marathon Ticket Alert"
    body = f"Found event info:\n\n{text}\n\nRegistration dates: {date}"

    send_email(
        subject,
        body,
        to_email="james@swinburn.co.uk",
        from_email="nionninga@gmail.com",
        app_password="arab iosp toip hbvr"
    )
