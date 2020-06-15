from control import Control

SECONDS_TO_WAIT = 86400

if __name__ == '__main__':
    print("Starting Birthday Reminder")
    control = Control()
    while True:
        try:
            control.check_events()
            break
            time.sleep(SECONDS_TO_WAIT)
        except Exception as ex:
            print(f"Exception while attempting to check events: {ex}")