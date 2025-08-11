import tkinter as tk
from tkinter import ttk
import time
import math

# --- Main App Window ---
root = tk.Tk()
root.title("Enhanced Clock App")
root.geometry("540x650")
root.configure(bg="#121212")

style = ttk.Style()
style.theme_use('clam')
style.configure('TNotebook.Tab', background='#1e1e1e', foreground='white', font=('Segoe UI', 13), padding=(10, 5))
style.map('TNotebook.Tab', background=[('selected', '#333333')])
style.configure('TFrame', background='#121212')
style.configure('TButton', font=('Segoe UI', 13), padding=12)
style.configure('TLabel', background='#121212', foreground='white', font=('Segoe UI', 28))

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both', pady=10)

# --- Clock Tab ---
clock_frame = ttk.Frame(notebook)
notebook.add(clock_frame, text='Clock')

# HH:MM:SS, :SS in cyan
digital_frame = tk.Frame(clock_frame, bg="#121212")
digital_frame.pack(pady=(40, 0))
time_label = tk.Label(digital_frame, font=("Segoe UI", 56), bg="#121212", fg="white")
time_label.pack(side="left")
seconds_label = tk.Label(digital_frame, font=("Segoe UI", 48), bg="#121212", fg="#8be9fd")
seconds_label.pack(side="left", padx=(5, 0))

# Analog clock canvas
canvas = tk.Canvas(clock_frame, width=420, height=420, bg="#1e1e1e", highlightthickness=0)
canvas.pack(expand=True, pady=(8, 0))

def update_clock():
    t = time.localtime()
    hr_min = time.strftime("%I:%M", t)
    ss = time.strftime("%S", t)
    ap = time.strftime("%p", t)
    time_label.config(text=f"{hr_min}")
    seconds_label.config(text=f":{ss}")
    time_label.update()
    seconds_label.update()

    # Analog clock
    canvas.delete("all")
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    radius = min(w, h) // 2 - 40
    cx, cy = w // 2, h // 2

    # Draw clock face
    canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill="#121212", outline="#444")

    for i in range(12):
        angle = math.radians(i * 30)
        x = cx + (radius - 20) * math.sin(angle)
        y = cy - (radius - 20) * math.cos(angle)
        canvas.create_text(x, y, text=str(i if i != 0 else 12), fill="white", font=("Segoe UI", 14))

    t = time.localtime()
    hr = t.tm_hour % 12 + t.tm_min / 60.0
    mn = t.tm_min + t.tm_sec / 60.0
    sc = t.tm_sec

    # Draw hands
    def draw_hand(length_ratio, angle_deg, color, width):
        angle = math.radians(angle_deg)
        x = cx + length_ratio * radius * math.sin(angle)
        y = cy - length_ratio * radius * math.cos(angle)
        canvas.create_line(cx, cy, x, y, fill=color, width=width, capstyle="round")

    draw_hand(0.5, hr * 30, "white", 7)      # Hour hand
    draw_hand(0.75, mn * 6, "#8be9fd", 5)    # Minute hand
    draw_hand(0.9, sc * 6, "red", 3)         # Second hand

    root.after(1000, update_clock)

update_clock()

# --- Timer Tab ---
timer_frame = ttk.Frame(notebook)
notebook.add(timer_frame, text='Timer')

timer_display = tk.Label(timer_frame, text="00:00:00", font=("Segoe UI", 64), bg="#121212", fg="white")
timer_display.pack(pady=(60, 32))

def set_preset(seconds):
    global remaining, timer_running
    timer_running = False
    remaining = seconds
    update_timer_display()

def update_timer_display():
    hrs, rem = divmod(remaining, 3600)
    mins, secs = divmod(rem, 60)
    timer_display.config(text=f"{hrs:02}:{mins:02}:{secs:02}")

def count_down():
    global remaining, timer_running
    if timer_running and remaining > 0:
        remaining -= 1
        update_timer_display()
        root.after(1000, count_down)
    else:
        timer_running = False

def toggle_timer():
    global timer_running
    if not timer_running and remaining > 0:
        timer_running = True
        count_down()

remaining = 0
timer_running = False

# Preset buttons
preset_frame = tk.Frame(timer_frame, bg="#121212")
preset_frame.pack(pady=12)

presets = [
    (60, "1m"), (300, "5m"), (600, "10m"),
    (1_200, "20m"), (1_800, "30m"),
    (3_600, "1h"), (7_200, "2h"), (10_800, "3h"),
    (18_000, "5h"), (36_000, "10h")
]

for secs, label in presets:
    b = tk.Button(preset_frame, text=label, command=lambda s=secs: set_preset(s),
                  bg="#333", fg="white", font=('Segoe UI', 15),
                  relief="flat", width=8, height=2, bd=0)
    b.pack(side="left", padx=8, pady=5)

timer_button = tk.Button(timer_frame, text="Start", command=toggle_timer,
                         font=("Segoe UI", 18), bg="#222", fg="white", relief="flat", height=2, width=15)
timer_button.pack(pady=18)

# --- Stopwatch Tab ---
stopwatch_frame = ttk.Frame(notebook)
notebook.add(stopwatch_frame, text='Stopwatch')

stopwatch_time = tk.Label(stopwatch_frame, text="00:00.00", font=("Segoe UI", 64), bg="#121212", fg="white")
stopwatch_time.pack(pady=(70, 32))

sw_running = False
sw_start_time = 0
sw_elapsed = 0

def update_stopwatch():
    if sw_running:
        now = time.time()
        delta = sw_elapsed + (now - sw_start_time)
        minutes = int(delta // 60)
        seconds = int(delta % 60)
        ms = int((delta - int(delta)) * 100)
        stopwatch_time.config(text=f"{minutes:02}:{seconds:02}.{ms:02}")
        root.after(10, update_stopwatch)

def toggle_stopwatch():
    global sw_running, sw_start_time
    if not sw_running:
        sw_start_time = time.time()
        sw_running = True
        update_stopwatch()

def reset_stopwatch():
    global sw_running, sw_elapsed
    sw_running = False
    sw_elapsed = 0
    stopwatch_time.config(text="00:00.00")

button_frame = tk.Frame(stopwatch_frame, bg="#121212")
button_frame.pack(pady=10)
tk.Button(button_frame, text="Start", command=toggle_stopwatch,
          font=("Segoe UI", 18), bg="#222", fg="white", relief="flat", width=12, height=2).pack(side="left", padx=10)
tk.Button(button_frame, text="Reset", command=reset_stopwatch,
          font=("Segoe UI", 18), bg="#444", fg="white", relief="flat", width=12, height=2).pack(side="left", padx=10)

root.mainloop()
