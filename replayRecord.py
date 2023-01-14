from pynput import keyboard
import logging
from time import time, sleep


def record_log(log_filename='cha_cha_slide.log'):
    logging.basicConfig(filename=log_filename,
                        level=logging.DEBUG, filemode='w', format='%(message)s')

    def on_press(key):
        if hasattr(key, 'char'):
            current = key.char
        else:
            current = key.name
        timestamp = time.perf_counter()
        logging.info(f'{timestamp} press {current}')

    def on_release(key):
        if hasattr(key, 'char'):
            current = key.char
        else:
            current = key.name
        timestamp = time.perf_counter()
        logging.info(f'{timestamp} release {current}')

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def replay_log(log_filename='cha_cha_slide.log'):
    prev_timestamp = 0
    keyboard_controller = keyboard.Controller()

    def on_key_event(key, key_event):
        if key_event == "None":
            return
        try:
            getattr(keyboard_controller, key_event)(key)
        except ValueError:
            getattr(keyboard_controller, key_event)(keyboard.Key[key])
        except:
            print("Error")

    with open(log_filename, "r") as f:
        for line in f:
            timestamp, key_event, key = line.strip().split(" ")
            timestamp = float(timestamp)
            if prev_timestamp != 0:
                time_to_sleep = timestamp - prev_timestamp
                sleep(time_to_sleep)
            on_key_event(key, key_event)
            prev_timestamp = timestamp
