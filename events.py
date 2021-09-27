import datetime
from googleapiclient.discovery import build
from credentials import CredsManager
from notifications import NotificationSender
import logging_setup


logger = logging_setup.get_logger("events")


class BirthdayEvent:
    def __init__(self, who, when_datetime):
        """
        Class representing a birthday event, with some basic info about the event.

        :param str who: Name of person who the birthday event corresponds to.
        :param datetime when_datetime: datetime of when the birthday event is.
        """
        self.who = who
        self.when_datetime = when_datetime
        self.days_until = self.calculate_days_until(when_datetime)

    def to_dict(self):
        return {
            "who": self.who,
            "when_datetime": str(self.when_datetime),
            "days_until": self.days_until,
        }

    @staticmethod
    def calculate_days_until(when_datetime, now=None):
        now_datetime = now if now else datetime.datetime.now()
        try:
            days_until = (when_datetime - now_datetime).days
        except TypeError as ex:
            logger.exception(
                f"Exception when trying to calculate days until event: {ex}"
            )
            raise ex
        seconds_since_midnight = (
            now_datetime
            - now_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        ).total_seconds()
        # Todo: This +1 for seconds after midnight is BS and needs to be removed
        if seconds_since_midnight:
            days_until += 1
        return days_until

    def __str__(self):
        return (
            f"BirthdayEvent object (who: `{self.who}`, when_datetime: "
            f"`{self.when_datetime}`, days_until: `{self.days_until}`)"
        )

    def __repr__(self):
        return (
            f"BirthdayEvent object (who: `{self.who}`, when_datetime: "
            f"`{self.when_datetime}`, days_until: `{self.days_until}`)"
        )


class EventRetriever:
    def __init__(self, creds):
        self.creds = creds
        self.service = build("calendar", "v3", credentials=creds)

    def _parse_event(self, event_dict):
        who = event_dict["summary"].split("'")[0]
        when_str = event_dict["start"]["date"]
        when_datetime = datetime.datetime.strptime(when_str, "%Y-%m-%d")
        return BirthdayEvent(who, when_datetime)

    def retrieve_events(self):
        now = datetime.datetime.utcnow().isoformat() + "Z"
        logger.info("Getting the upcoming birthday events")
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
        events = events_result.get("items", [])
        return [self._parse_event(event) for event in events]


class EventChecker:
    def __init__(
        self, creds_manager=None, event_retriever=None, notifications=None
    ):
        if not creds_manager:
            self._creds_manager = CredsManager()
        if not event_retriever:
            self._event_retriever = EventRetriever(self._creds_manager.creds)
        if not notifications:
            self._notifications = NotificationSender()

    def check_events(self, warn_days=None):
        if not warn_days:
            warn_days = [30, 14, 7, 5, 0]
        events = self._event_retriever.retrieve_events()
        logger.debug("Retrieved events: %r ", events)
        logger.info(f"Retrieved {len(events)} events")
        logger.debug("Warn days: %r", warn_days)
        events_to_notify = [
            event for event in events if event.days_until in warn_days
        ]
        logger.debug("Events to notify: %r ", events_to_notify)
        logger.info(f"Sending notifications for {len(events_to_notify)} events")
        for event in events_to_notify:
            self._notifications.notify_event(event)
