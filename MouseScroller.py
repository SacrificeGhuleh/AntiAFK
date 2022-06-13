import pystray
from PIL import Image, ImageDraw

from threading import Timer
from pyautogui import scroll, press

direction = 1
speed = 100

active = True


def activate():
    global active
    active = not active


def isActive(v):
    global active
    return active


def scrollFn():
    if not active:
        return

    global direction
    direction *= -1
    scroll(direction)
    press('f15')


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def exit():
    repeatTimer.cancel()
    icon.stop()


def createImage(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image


icon = pystray.Icon(
    name='AntiAFK',
    title='AntiAFK',
    icon=createImage(64, 64, 'black', 'white'),
    menu=pystray.Menu(
        pystray.MenuItem(
            "Active",
            activate,
            checked=isActive,
            radio=True
        ),
        pystray.MenuItem(
            "Exit",
            exit
        )
    )
)

repeatTimer = RepeatTimer(speed, scrollFn)
repeatTimer.start()
icon.run()
