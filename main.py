from control import Control
import time
import schedule


control = Control()

def check_for_events():
    try:
        control.check_events()
    except Exception as ex:
        print(f"Exception while attempting to check events: {ex}")

schedule.every().day.at("09:00").do(check_for_events)

if __name__ == '__main__':
    print("Starting Birthday Reminder")
    while True:
        schedule.run_pending()
        time.sleep(1)
