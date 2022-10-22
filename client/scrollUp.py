from pynput.keyboard import Key, Controller
from time import sleep

keyboard = Controller() 
dur = 0.05 * 60
offset = 0.15 * 60

sleep(offset)
while True:
    keyboard.press(Key.ctrl_l)
    keyboard.press(Key.home)
    keyboard.release(Key.ctrl_l)
    keyboard.release(Key.home)
    sleep(dur)