from pynput import keyboard
import logging
import time

def record_log(log_filename='cha_cha_slide.log'):
    logging.basicConfig(filename=log_filename, level=logging.DEBUG, filemode='w', format='%(message)s')
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

    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
