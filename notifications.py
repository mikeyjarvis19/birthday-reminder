import requests
import json
import logging_setup


logger = logging_setup.get_logger("notifications")


class PushoverNotifications:
    def __init__(self):
        credentials = json.loads(open("pushover_credentials.json").read())
        self.url = "https://api.pushover.net/1/messages.json"
        self.user = credentials["user"]
        self.token = credentials["token"]

    def send_notification(self, title, message):
        data = {
            "user": self.user,
            "token": self.token,
            "title": title,
            "message": message,
        }
        response = requests.post(self.url, data=data)
        logger.info(
            f"Retrieved response code: '{response.status_code}' from '{self.url}'"
        )
        return response.status_code


class NotificationSender:
    def __init__(self, service=None):
        self.service = service if service else PushoverNotifications()

    def build_message(self, birthday_event):
        title = (
            f"It's {birthday_event.who}'s birthday "
            f"{'today' if birthday_event.days_until == 0 else 'soon'}!"
        )
        message = (
            f"It's in {birthday_event.days_until} days! "
            f"({birthday_event.when_datetime.strftime('%d-%m-%Y')})"
            if birthday_event.days_until > 0
            else "Happy Birthday!"
        )
        return title, message

    def notify_event(self, birthday_event):
        title, message = self.build_message(birthday_event)
        self.service.send_notification(title, message)
