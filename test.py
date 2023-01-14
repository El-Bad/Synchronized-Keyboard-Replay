import tkinter as tk

def on_press():
    global is_recording
    if is_recording:
        # Stop recording
        button.config(text="Start Recording")
        indicator.config(bg="white")
        is_recording = False
    else:
        # Start recording
        button.config(text="Stop Recording")
        indicator.config(bg="red")
        is_recording = True

root = tk.Tk()
is_recording = False
frame = tk.Frame(root)
frame.pack()

button = tk.Button(frame, text="Start Recording", command=on_press)
button.pack(side = tk.LEFT)
indicator = tk.Label(frame, bg="white", width=10, height=10)
indicator.pack(side = tk.LEFT)
root.mainloop()
