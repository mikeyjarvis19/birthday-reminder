from events import EventChecker
import time
import schedule
import logging_setup

logger = logging_setup.get_logger("main")
event_checker = EventChecker()


def check_for_events():
    try:
        event_checker.check_events()
    except Exception as ex:
        logger.exception(f"Exception while attempting to check events: {ex}")


schedule.every().day.at("09:00").do(check_for_events)

if __name__ == "__main__":
    logger.info("Starting Birthday Reminder")
    while True:
        check_for_events()
        # schedule.run_pending()
        time.sleep(5)
