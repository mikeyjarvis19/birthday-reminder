import pytest
from events import EventRetriever
from credentials import CredsManager
from events import BirthdayEvent
from notifications import PushoverNotifications


def test_event_retrieval():
    creds_manager = CredsManager()
    event_retriever = EventRetriever(creds_manager.creds)
    events = event_retriever.retrieve_events()
    assert len(events) > 0
    for event in events:
        assert isinstance(event, BirthdayEvent)
        assert all(
            hasattr(event, attr)
            for attr in ["days_until", "when_datetime", "who"]
        )

def test_notification_sending():
    notifications = PushoverNotifications()
    test_title = "TEST TITLE"
    test_message = "TEST MESSAGE"
    response_code = notifications.send_notification(test_title, test_message)
    assert response_code == 200
