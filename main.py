from control import Control
import time
import schedule
import logging_setup

logger = logging_setup.get_logger("main")
control = Control()

def check_for_events():
    try:
        control.check_events()
    except Exception as ex:
        logger.error(f"Exception while attempting to check events: {ex}")

schedule.every().day.at("09:00").do(check_for_events)

if __name__ == '__main__':
    logger.info("Starting Birthday Reminder")
    while True:
        schedule.run_pending()
        time.sleep(1)
