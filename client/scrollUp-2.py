from pynput.mouse import Controller
from time import sleep

mouse = Controller()
dur = 0.1 * 60
offset = 0.15 * 60

sleep(offset)
while True:
    mouse.scroll(0, 10)
    print("d")
    sleep(dur)