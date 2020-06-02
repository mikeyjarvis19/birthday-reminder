import requests
import json


class PushoverNotifications:

    def __init__(self):
        credentials = json.loads(open("../pushover_credentials.json").read())
        self.url = "https://api.pushover.net/1/messages.json"
        self.user = credentials["user"]
        self.token = credentials["token"]

    def send_notification(self, title, message):
        data = {"user": self.user, "token": self.token, "title": title,
                "message": message}
        response = requests.post(self.url, data=data)
        print(f"Retrieved response code: '{response.status_code}' from '{self.url}'")

