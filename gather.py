from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class BirthdayEvent():

    def __init__(self, who, when_datetime):
        self.who = who
        self.when_datetime = when_datetime
        self.days_until = (when_datetime - datetime.datetime.now()).days


def parse_event(event_dict):
    who = event_dict['summary'].split("\'")[0]
    when_str = event_dict['start']['date']
    when_datetime = datetime.datetime.strptime(when_str, '%Y-%m-%d')
    return BirthdayEvent(who, when_datetime)


def alert_birthday(birthday_event, warn_within_days=190):
    if birthday_event.days_until <= warn_within_days:
        print(
            f"It's {birthday_event.who}'s birthday in "
            f"{birthday_event.days_until} days!"
        )


def main():
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
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming birthday events")
    events_result = (
        service.events()
        .list(
            calendarId="addressbook#contacts@group.v.calendar.google.com",
            timeMin=now,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    if not events:
        print("No upcoming events found.")
    for event in events:
        birthday_event = parse_event(event)
        alert_birthday(birthday_event)



if __name__ == "__main__":
    main()
