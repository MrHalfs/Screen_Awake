import pyautogui
from datetime import datetime, timedelta, time as time2
import schedule
import time
import sys


class Screen:
    def __init__(self, start: tuple, mode="office"):
        self.start = time2(start[0], start[1], start[2])
        self.end = None
        self.mode = mode
        if self.mode == "office":
            self.end = time2(6, 50, 0)
        elif self.mode == "home":
            self.end = time2(7, 55, 0)

    def send_alert(self):
        if not self.alert_status():
            x, y = pyautogui.position()
            # company policies require exagerated movement. otherwise set the values to 1 and remove keyboard press
            pyautogui.moveTo(x - 100, y)
            pyautogui.moveTo(x + 100, y)
            pyautogui.moveTo(x, y)
            pyautogui.press("ctrl", presses=2)
            print(f'Input at: {datetime.now().time().strftime("%H:%M:%S")}')

    def alert_status(self):
        answer = pyautogui.confirm(text="You There?", title="User Status", buttons=["Yes", "No"], timeout=30000)
        if answer == "Timeout":
            return False
        elif answer == "Yes" or answer == "No":
            return True


def main():
    modes = ["office", "home"]
    while True:
        mode = input("Work location (home/office): ").lower().strip()
        if mode not in modes:
            print("Invalid option")
        else:
            mover = Screen((0, 1, 0), mode=mode)
            break
    print(f"Mouse will move between: {mover.start} AM - {mover.end} AM")
    schedule.every(9).minutes.do(mover.send_alert)
    while True:
        current = datetime.now().time()
        try:
            if mover.start < current < mover.end:
                schedule.run_pending()
            else:
                continue
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting Program")
            sys.exit(1)


if __name__ == "__main__":
    main()
