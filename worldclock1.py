import tkinter as tk
from datetime import datetime
import pytz
import tzlocal  # to detect local timezone

# --- Define city names and their timezone strings ---
CITIES = {
    "Delhi 🇮🇳": "Asia/Kolkata",
    "London 🇬🇧": "Europe/London",
    "New York 🇺🇸": "America/New_York",
    "Sydney 🇦🇺": "Australia/Sydney",
    "Dubai 🇦🇪": "Asia/Dubai",
    "Rio de Janeiro 🇧🇷": "America/Sao_Paulo",
    "Tokyo 🇯🇵": "Asia/Tokyo",
   "Paris 🇫🇷": "Europe/Paris"
}

# --- Detect local timezone safely ---
local_tz_obj = tzlocal.get_localzone()
local_tz = getattr(local_tz_obj, "zone", str(local_tz_obj))

# --- Create the main window ---
root = tk.Tk()
root.title("🌍 World Clock")
root.geometry("640x480")
root.resizable(False, False)

# --- Create gradient background using Canvas ---
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack(fill="both", expand=True)

def draw_gradient():
    """Draws a vertical gradient from dark blue to purple."""
    color1 = (10, 20, 40)   # dark navy
    color2 = (60, 0, 90)    # purple
    steps = 480
    for i in range(steps):
        r = int(color1[0] + (color2[0] - color1[0]) * i / steps)
        g = int(color1[1] + (color2[1] - color1[1]) * i / steps)
        b = int(color1[2] + (color2[2] - color1[2]) * i / steps)
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, 640, i, fill=color, width=1)

draw_gradient()

# --- Title Label ---
title = tk.Label(root, text="🌎 World Clock", font=("Segoe UI", 22, "bold"),
                 fg="#00d4ff", bg="#1a1a40")
canvas.create_window(320, 30, window=title)

# --- Frame for city clocks ---
frame = tk.Frame(root, bg="#000000", highlightthickness=0)
canvas.create_window(320, 240, window=frame)

# --- Create labels for each city (fixed alignment) ---
labels = {}
for i, (city, tz) in enumerate(CITIES.items()):
    is_local = (tz == local_tz)

    row_frame = tk.Frame(frame, bg="#000000")
    row_frame.grid(row=i, column=0, padx=25, pady=8, sticky="ew")
    row_frame.grid_columnconfigure(0, weight=1)
    row_frame.grid_columnconfigure(1, weight=1)

    city_label = tk.Label(
        row_frame,
        text=city + (" ⭐" if is_local else ""),
        font=("Segoe UI", 14, "bold"),
        fg="#00ff99" if is_local else "#00d4ff",
        bg="#000000",
        anchor="w"
    )
    city_label.grid(row=0, column=0, sticky="w")

    time_label = tk.Label(
        row_frame,
        text="--:--:-- --",
        font=("Consolas", 16, "bold"),
        fg="#e6eef8",
        bg="#000000",
        anchor="e"
    )
    time_label.grid(row=0, column=1, sticky="e")

    labels[city] = (time_label, tz)

# --- Time format state (12 or 24 hour) ---
is_24hr = tk.BooleanVar(value=False)

# --- Function to update all clocks ---
def update_time():
    fmt_12 = "%I:%M:%S %p"
    fmt_24 = "%H:%M:%S"
    fmt = fmt_24 if is_24hr.get() else fmt_12

    for city, (label, tz) in labels.items():
        timezone = pytz.timezone(tz)
        city_time = datetime.now(timezone)
        formatted_time = city_time.strftime(fmt)
        label.config(text=formatted_time)
    root.after(1000, update_time)  # update every second

# --- Toggle format function ---
def toggle_format():
    is_24hr.set(not is_24hr.get())
    format_btn.config(
        text="12-Hour" if is_24hr.get() else "24-Hour"
    )

# --- Button for toggling format ---
format_btn = tk.Button(
    root,
    text="24 hrs",
    font=("Segoe UI", 10, "bold"),
    bg="#1a1a40",
    fg="#00ffcc",
    activebackground="#333366",
    activeforeground="#00ffcc",
    borderwidth=0,
    highlightthickness=0,
    command=toggle_format
)
canvas.create_window(580, 450, window=format_btn)  # Moved to right bottom

# --- Start updating ---
update_time()

# --- Footer ---
footer = tk.Label(root, text="Auto-updating every second  |  Toggle 12H / 24H  |  Gradient background",
                  font=("Segoe UI", 9), fg="#aaaaaa", bg="#000000")
canvas.create_window(320, 460, window=footer)

# --- Run the app ---
root.mainloop()



