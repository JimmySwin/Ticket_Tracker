from src.db_manager import create_table, get_all_events
from notify.emailer import get_notification_events, send_email_notification

def main():
    create_table()
    events = get_all_events()
    notifications = get_notification_events(events)
    send_email_notification(notifications, "james@swinburn.co.uk")

if __name__ == "__main__":
    main()