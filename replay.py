from pynput import keyboard
import logging
import time

log_filename = 'cha_cha_slide.log'

prev_timestamp = 0
prev_key = ""

def on_press(key):
    try:
        current = str(key)
    except ValueError:
        keyboard_controller.press(keyboard.Key[key])

def on_release(key):
    try:
        keyboard_controller.release(key)
    except ValueError:
        keyboard_controller.release(keyboard.Key[key])

keyboard_controller = keyboard.Controller()

with open(log_filename, "r") as f:
    for line in f:
        timestamp, key_event, key = line.strip().split(" ")
        timestamp = float(timestamp)
        if prev_timestamp != 0:
            time_to_sleep = timestamp - prev_timestamp
            time.sleep(time_to_sleep)
        if key_event == "pressed":
            on_press(key)
        elif key_event == "released":
            on_release(key)
        prev_timestamp = timestamp
        prev_key = key
