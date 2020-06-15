import datetime
import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from notifications import PushoverNotifications


class CredsManager:
    """Setup creds"""

    def __init__(self):
        self.creds = self.setup_creds()

    def setup_creds(self):
        scopes = ["https://www.googleapis.com/auth/calendar.readonly"]
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", scopes
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return creds


class EventRetriever:
    def __init__(self, creds):
        self.creds = creds
        self.service = build("calendar", "v3", credentials=creds)

    def retrieve_events(self):
        now = datetime.datetime.utcnow().isoformat() + "Z"
        print("Getting the upcoming birthday events")
        events_result = (
            self.service.events()
            .list(
                calendarId="addressbook#contacts@group.v.calendar.google.com",
                timeMin=now,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result.get("items", [])


class BirthdayEvent:
    def __init__(self, who, when_datetime):
        self.who = who
        self.when_datetime = when_datetime
        self.days_until = (when_datetime - datetime.datetime.now()).days + 1

    def to_dict(self):
        return {
            "who": self.who,
            "when_datetime": str(self.when_datetime),
            "days_until": self.days_until,
        }


class Control:
    def __init__(self):
        self._creds_manager = CredsManager()
        self._event_retriever = EventRetriever(self._creds_manager.creds)
        self._notifications = PushoverNotifications()

    def _parse_event(self, event_dict):
        who = event_dict["summary"].split("'")[0]
        when_str = event_dict["start"]["date"]
        when_datetime = datetime.datetime.strptime(when_str, "%Y-%m-%d")
        return BirthdayEvent(who, when_datetime)

    def get_events(self):
        events = self._event_retriever.retrieve_events()
        return [self._parse_event(event) for event in events]

    def check_events(self, warn_days=None):
        if not warn_days:
            warn_days = range(0, 30)
        events = self.get_events()
        for event in events:
            if event.days_until in warn_days:
                self.notify_event(event)

    def notify_event(self, birthday_event):
        title = f"It's {birthday_event.who}'s birthday soon!"
        message = (
            f"It's in {birthday_event.days_until} days! "
            f"({birthday_event.when_datetime.strftime('%d-%m-%Y')})"
        )
        self._notifications.send_notification(title, message)
