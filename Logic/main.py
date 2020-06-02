from Logic.control import Control
import time

if __name__ == '__main__':
    print("Starting Birthday Reminder")
    control = Control()
    while True:
        try:
            control.check_events()
            time.sleep(15)
        except Exception as ex:
            print(f"Exception while attempting to check events: {ex}")