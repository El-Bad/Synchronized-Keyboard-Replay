from pynput import keyboard
import logging
import time
from datetime import datetime, timedelta
import ntplib
from datetime import datetime, timezone


def getNTPTime(timezone=timezone.utc):
    c = ntplib.NTPClient()
    response = c.request('time.windows.com', version=3)
    current_time = datetime.fromtimestamp(response.tx_time)
    return current_time.astimezone(timezone)


def record_log(log_filename='cha_cha_slide.log'):
    logging.basicConfig(filename=log_filename,
                        level=logging.DEBUG, filemode='w', format='%(message)s')
    pressedKeys = set()

    def on_press(key):
        if hasattr(key, 'char'):
            current = key.char
        else:
            current = key.name

        if current in pressedKeys:
            return
        pressedKeys.add(current)

        timestamp = time.perf_counter()
        logging.info(f'{timestamp} press {current}')

    def on_release(key):
        if hasattr(key, 'char'):
            current = key.char
        else:
            current = key.name

        if current not in pressedKeys:
            return
        pressedKeys.remove(current)

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
                time.sleep(time_to_sleep)
            on_key_event(key, key_event)
            prev_timestamp = timestamp


def replay_at_utc(input_time, log_filename='cha_cha_slide.log', offset=0):
    current_time = getNTPTime()
    print("Current time (UTC):", current_time.strftime("%H:%M:%S %Y-%m-%d"))

    target_time = datetime.strptime(input_time, "%H:%M:%S")
    target_time = current_time.replace(hour=target_time.hour,
                                       minute=target_time.minute,
                                       second=target_time.second,
                                       microsecond=0)

    offset = timedelta(milliseconds=offset)
    target_time += offset

    if target_time < getNTPTime():
        target_time += timedelta(days=1)

    sleep_time = (target_time - getNTPTime()).total_seconds()
    print("Starting in:", sleep_time, "seconds")
    time.sleep(sleep_time)
    print("Started replaying at:", target_time)
    replay_log(log_filename)
    print("done")
