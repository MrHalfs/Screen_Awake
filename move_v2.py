import pyautogui
from datetime import datetime, timedelta, time as time2
import schedule
import time
import sys
import mouse
from mouse import _MouseListener, hook, LEFT


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
        # if not self.alert_status():
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


class MouseEvent:
    def __init__(self):
        self.moved = False
        self.xy = (0, 0)

    def on_move(self, event):
        self.moved = True
        x, y = mouse.get_position()
        self.xy = (x, y)

    def non_move(self):
        self.moved = False

    def moved_status(self, x, y):
        print((x, y), "|", self.xy)
        pos = []
        for i, j in zip((x, y), self.xy):
            if abs(i - j) <= 2:
                pos.append(True)
            else:
                pos.append(False)
        return all(pos)


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
    event = MouseEvent()
    print("\nClick to start")
    mouse.hook(event.on_move)
    mouse.wait(button=LEFT)
    event.non_move()
    time_passed = 0
    mouse_sleep = 0
    while True:
        x, y = mouse.get_position()
        if event.moved_status(x, y):
            mouse_sleep += 1
        else:
            mouse_sleep = 0
            time_passed = 0
        if mouse_sleep >= 10:
            event.non_move()
        moved = event.moved
        if moved:
            time_passed = 0
        current = datetime.now().time()
        try:
            if mover.start < current < mover.end and not moved and time_passed > 540:
                mover.send_alert()
                time_passed = 0
                time.sleep(1)
            else:
                time_passed += 1
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting Program")
            sys.exit(1)


if __name__ == "__main__":
    main()
