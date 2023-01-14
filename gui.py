import tkinter as tk
from time import sleep
from datetime import datetime, timezone, timedelta
import sync
from replayRecord import record_log, replay_at_utc
import threading

offset = 0
is_recording = False
is_replaying = False


def record():
    log_filename = filename_entry.get()
    global is_recording
    if is_recording:
        record_button.config(bg=root.cget('bg'), text="Record")
        is_recording = False
        print("Stopped recording")
    else:
        record_button.config(bg="red", text="Record")
        is_recording = True
        print("Recording to", log_filename)
        threading.Thread(target=record_log,
                         args=((log_filename,))).start()


def replay():
    input_time = input_entry.get()
    log_filename = filename_entry.get()
    if input_time == "":
        print("Replaying in 3 seconds...")
    else:
        print("Replaying at", input_time)
        threading.Thread(target=replay_at_utc,
                         args=((input_time, log_filename))).start()


def update_time():
    global offset
    current_time = datetime.utcnow() + offset
    current_time = current_time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    root.after(1000, update_time)


def update_time_offset():
    global offset
    utc_time = datetime.now().astimezone(timezone.utc)
    ntp_time = sync.getNTPTime().replace(tzinfo=timezone.utc)
    offset_in_seconds = (ntp_time - utc_time).total_seconds()
    offset_in_milliseconds = offset_in_seconds * 1000
    offset = timedelta(milliseconds=offset_in_milliseconds)
    root.after(30000, update_time_offset)


root = tk.Tk()
root.title("Keyboard Recorder")

record_button = tk.Button(root, text="Record", command=record)
record_button.grid(row=0, column=0, padx=10, pady=10)

filename_entry = tk.Entry(root)
filename_entry.insert(0, "cha_cha_slide.log")
filename_entry.grid(row=0, column=1, padx=10, pady=10)

divider = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
divider.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

replay_button = tk.Button(root, text="Replay", command=replay)
replay_button.grid(row=2, column=0, padx=10, pady=10)

input_entry = tk.Entry(root)
input_entry.grid(row=2, column=1, padx=10, pady=10)

clock_label = tk.Label(root, text="00:00:00", font=("Helvetica", 16))
clock_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

update_time_offset()
update_time()
root.mainloop()
