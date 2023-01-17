import tkinter as tk
import time
from datetime import datetime, timezone, timedelta
from replayRecord import record_log, replay_at_utc, getNTPTime
import multiprocessing

offset = 0
replayThread = None
recordThread = None
isReplaying = False
isRecording = False


def record():
    log_filename = filename_entry.get()
    global recordThread, isRecording
    if recordThread is None:
        record_button.config(bg="red", text="Stop Recording")
        print(f"Recording to {log_filename}")
        recordThread = multiprocessing.Process(
            target=record_log, args=(log_filename,))
        recordThread.start()
        isRecording = True
    else:
        print("Stopping recording...")
        recordThread.terminate()
        recordThread = None
        record_button.config(bg=root.cget('bg'), text="Record")
        isRecording = False


def replay():
    global replayThread, isReplaying, offset
    input_time = start_time_entry.get()
    log_filename = filename_entry.get()
    user_entry_offset = offset_entry.get()
    user_offset = 0
    if user_entry_offset != "":
        user_offset = int(user_entry_offset)

    if input_time == "":
        print("Replaying in 3 seconds...")
        input_time = datetime.utcnow() + offset + timedelta(seconds=3)
        input_time = input_time.strftime("%H:%M:%S")
    else:
        print(f"Replaying at {input_time} with offset {user_offset}ms...")

    try:
        datetime.strptime(input_time, "%H:%M:%S")
    except:
        print("Invalid time format")
        return

    if replayThread is None:
        replay_button.config(bg="red", text="Stop Replay")
        replayThread = multiprocessing.Process(target=replay_at_utc,
                                               args=(input_time, log_filename, user_offset))
        replayThread.start()
        isReplaying = True
    else:
        replayThread.terminate()
        replayThread = None
        replay_button.config(bg=root.cget('bg'), text="Replay")
        isReplaying = False


def update_time():
    global offset, isReplaying, replayThread
    current_time = datetime.utcnow() + offset
    current_time = current_time.strftime("%H:%M:%S")
    if not start_time_entry.touched:
        start_time_entry.fill_placeholder(current_time)
    if start_time_entry.get() == current_time and not start_time_entry.inFocus:
        start_time_entry.touched = False
        start_time_entry.config(fg='grey50')
    clock_label.config(text=current_time)
    root.after(100, update_time)
    if isReplaying and not replayThread.is_alive():
        replay_button.config(bg=root.cget('bg'), text="Replay")
        isReplaying = False
        replayThread = None

    if isRecording:
        replay_button["state"] = "disabled"
        filename_entry["state"] = "disabled"
        status_label.config(text="Recording...")
    elif isReplaying:
        record_button["state"] = "disabled"
        filename_entry["state"] = "disabled"
        start_time_entry["state"] = "disabled"
        offset_entry["state"] = "disabled"
        status_label.config(text="Replaying...")
    else:
        replay_button["state"] = "normal"
        record_button["state"] = "normal"
        filename_entry["state"] = "normal"
        start_time_entry["state"] = "normal"
        offset_entry["state"] = "normal"
        status_label.config(text="Ready")


def update_time_offset():
    global offset
    utc_time = datetime.now().astimezone(timezone.utc)
    ntp_time = getNTPTime().replace(tzinfo=timezone.utc)
    offset_in_seconds = (ntp_time - utc_time).total_seconds()
    offset_in_milliseconds = offset_in_seconds * 1000
    offset = timedelta(milliseconds=offset_in_milliseconds)
    root.after(30000, update_time_offset)


def validate_integer(P):
    if P.strip() == "":
        return True
    if P.isdigit():
        return True
    return False


class PlaceholderEntry(tk.Entry):
    touched = False
    placeholder = ""
    inFocus = False

    def __init__(self, master=None, placeholder='', cnf={}, fg='black',
                 fg_placeholder='grey50', *args, **kw):
        super().__init__(master=None, cnf={}, bg='white', *args, **kw)
        self.fg = fg
        self.fg_placeholder = fg_placeholder
        self.placeholder = placeholder
        self.bind('<FocusOut>', lambda event: self.fill_placeholder())
        self.bind('<FocusIn>', lambda event: self.clear_box())
        self.fill_placeholder()

    def clear_box(self):
        self.inFocus = True
        self.config(fg=self.fg)
        self.touched = True

    def fill_placeholder(self, new_placeholder=None):
        if super().get() == '':
            self.touched = False
        if new_placeholder is not None:
            self.placeholder = new_placeholder
            self.delete(0, 'end')
            self.insert(0, self.placeholder)
        else:
            self.inFocus = False

        if not super().get():
            self.config(fg=self.fg_placeholder)
            self.insert(0, self.placeholder)
            self.inFocus = False

    def get(self):
        content = super().get()
        if content == self.placeholder:
            return ''
        return content


def on_closing():
    print("closing...")
    if recordThread is not None:
        recordThread.terminate()
    if replayThread is not None:
        replayThread.terminate()
    root.destroy()


if __name__ == "__main__":
    process = None
    root = tk.Tk()

    root.title("Keyboard Recorder")

    status_label = tk.Label(root, text="Ready", font=(
        "Helvetica", 16), justify=tk.CENTER)
    status_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    filename_label = tk.Label(root, text="Log file name:")
    filename_label.grid(row=1, column=0, padx=10, pady=0)

    filename_entry = tk.Entry(root)
    filename_entry.insert(0, "cha_cha_slide.log")
    filename_entry.grid(row=1, column=1, padx=10, pady=0)

    start_time_label = tk.Label(root, text="Start time:")
    start_time_label.grid(row=2, column=0, padx=10, pady=10)

    start_time_entry = PlaceholderEntry(
        root, datetime.utcnow().strftime("%H:%M:%S"))
    start_time_entry.grid(row=2, column=1, padx=10, pady=10)

    offset_label = tk.Label(root, text="offset (ms)")
    offset_label.grid(row=3, column=0)

    offset_entry = tk.Entry(root, validate="key", validatecommand=(
        root.register(validate_integer), '%P'))
    offset_entry.insert(0, "0")
    offset_entry.grid(row=3, column=1)

    divider = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
    divider.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

    record_button = tk.Button(root, text="Record", command=record, width=15)
    record_button.grid(row=5, column=0, padx=10, pady=10)

    replay_button = tk.Button(root, text="Replay", command=replay, width=15)
    replay_button.grid(row=5, column=1, padx=10, pady=10)

    utc_label = tk.Label(root, text="Current UTC Time:")
    utc_label.grid(row=6, column=0)
    clock_label = tk.Label(root, text="00:00:00", font=("Helvetica", 16))
    clock_label.grid(row=6, column=1)

    starting_at_label = tk.Label(root, text="Starting replay at:")
    starting_at_label.grid(row=7, column=0)
    target_label = tk.Label(root, text="", font=("Helvetica", 16))
    target_label.grid(row=7, column=1)

    update_time_offset()
    update_time()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
