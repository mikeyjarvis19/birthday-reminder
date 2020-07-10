import pytest
from events import BirthdayEvent
import datetime

# import logging


class TestBirthdayEvent:
    def test_init_birthday_event_good_values(self):
        who = "Bob"
        when = datetime.datetime.now()
        event = BirthdayEvent(who, when)
        assert event.who == who
        assert event.when_datetime <= datetime.datetime.now()

    def test_init_birthday_event_bad_when(self):
        # TODO: Assert log/ exception messages here + hide exceptions in logs.
        # with caplog.at_level(logging.CRITICAL, logger="root.baz") as log:
        with pytest.raises(TypeError) as ex:
            who = "Bob"
            now = "Right here, right now"
            BirthdayEvent(who, now)
        # assert "Exception when trying to calculate days until event" in log.text
        # assert (
        #     "Param 'when_datetime' should be of type 'datetime.datetime'"
        #     in ex.value.args[0]
        # )

    def test_birthday_event_to_dict(self):
        who = "Bob"
        when = datetime.datetime.now()
        event = BirthdayEvent(who, when)
        event_dict = event.to_dict()
        assert event_dict.get("who") == who
        assert event_dict.get("when_datetime") == str(when)

    def test_birthday_event_calculate_days_until_at_midnight(self):
        current_date = datetime.datetime(2020, 7, 10, 00, 00, 00)
        event_date = datetime.datetime(2020, 7, 15)
        expected_days_until = 5
        days_until = BirthdayEvent.calculate_days_until(event_date, current_date)
        assert days_until == expected_days_until

    def test_birthday_event_calculate_days_until_after_midnight(self):
        current_date = datetime.datetime(2020, 7, 10, 00, 00, 1)
        event_date = datetime.datetime(2020, 7, 15)
        expected_days_until = 5
        days_until = BirthdayEvent.calculate_days_until(event_date, current_date)
        assert days_until == expected_days_until
