import tkinter as tk
from tkinter import ttk
import webbrowser
import json
import os

courses = [
    ("AI + Python for Beginners", 
     "Learn the basics of Python and AI concepts. Perfect for absolute beginners.", 
     "https://www.deeplearning.ai/short-courses/ai-python-for-beginners/"),
    ("Vibe Coding 101 with Replit", 
     "Get started with coding in a fun, collaborative environment using Replit.", 
     "https://www.deeplearning.ai/short-courses/vibe-coding-101-with-replit"),
    ("Building an AI-Powered Game", 
     "Build an interactive game with AI integration from scratch.", 
     "https://www.deeplearning.ai/short-courses/building-an-ai-powered-game"),
    ("YouTube Livestreams: Lovable Labs", 
     "Watch live sessions and demos about AI app building on YouTube.", 
     "https://www.youtube.com/@lovable-labs"),
    ("YouTube Playlist: AI Builds Apps in 1 Hour", 
     "Explore a series of videos where AI builds apps in just 1 hour.", 
     "https://www.youtube.com/playlist?list=PLy9mLEnHHo4VP7p8kkHlDLPLYRacLzlTQ"),
     
]

PROGRESS_FILE = "progress.json"
course_widgets = []
notes = {}

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

def save_progress():
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"index": index, "notes": notes}, f)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                data = json.load(f)
                return data.get("index", 0), data.get("notes", {})
        except Exception:
            return 0, {}
    return 0, {}

def update_display():
    global index
    if 0 <= index < len(courses):
        title, desc, url = courses[index]
        label_title.config(text=f"Next Course ({index+1}/{len(courses)}): {title}")
        label_desc.config(text=f"Description: {desc}\n\nURL: {url}")
        button_next.config(text=f"{ordinal(index+1)} course", state="normal")
        restart_button.grid_remove()
        notes_text.config(state="normal")
        notes_text.delete("1.0", tk.END)
        if str(index) in notes:
            notes_text.insert(tk.END, notes[str(index)])
        notes_text.config(state="normal")
    else:
        label_title.config(text="🎉 All courses completed!")
        label_desc.config(text="Well done! You've visited all the resources.")
        button_next.config(state="disabled")
        restart_button.grid()
        notes_text.config(state="normal")
        notes_text.delete("1.0", tk.END)
        notes_text.config(state="disabled")
    progress_var.set(index)
    for i, widget in enumerate(course_widgets):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        prefix = "✅" if i < index else ("➡️" if i == index else "⬜")
        widget.insert(tk.END, f"{prefix} {ordinal(i+1)}: {courses[i][0]}")
        if i == index:
            widget.config(bg="#fff9d6")
        elif i < index:
            widget.config(bg="#e0ffe0")
        else:
            widget.config(bg="#f0f0f0")
        widget.config(state="disabled")
    save_progress()

def open_next():
    global index
    if 0 <= index < len(courses):
        url = courses[index][2]
        webbrowser.open(url)
        index += 1
        update_display()

def restart():
    global index
    index = 0
    update_display()
    button_next.config(state="normal")
    restart_button.grid_remove()

def on_course_click(event, idx):
    global index
    index = idx
    update_display()

def save_note(event=None):
    global notes, index
    notes[str(index)] = notes_text.get("1.0", tk.END).strip()
    save_progress()
    notes_text.edit_modified(False)
    check_notes_scrollbar()

def check_notes_scrollbar(event=None):
    total_lines = int(notes_text.index('end-1c').split('.')[0])
    try:
        first_visible = int(notes_text.index("@0,0").split('.')[0])
        last_visible = int(notes_text.index(f"@0,{notes_text.winfo_height()}").split('.')[0])
        visible_lines = last_visible - first_visible
    except Exception:
        visible_lines = int(notes_text['height'])
    if total_lines > visible_lines:
        notes_scrollbar.grid(row=5, column=1, sticky="ns", pady=(0, 10))
    else:
        notes_scrollbar.grid_remove()

# ---- App Start ----
index, notes = load_progress()

root = tk.Tk()
root.title("Learning URL Navigator")
root.geometry("1000x700")

# Responsive main layout with grid
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=0)
main_frame.grid_columnconfigure(1, weight=1)

# Left: Course List Overview (scrollable)
overview_frame = tk.Frame(main_frame)
overview_frame.grid(row=0, column=0, sticky="ns", padx=(0, 30))
overview_frame.grid_rowconfigure(0, weight=1)
overview_frame.grid_columnconfigure(0, weight=1)

# Canvas + Frame for scrollable course list
course_canvas = tk.Canvas(overview_frame, borderwidth=0, highlightthickness=0, width=350)
course_scrollbar = tk.Scrollbar(overview_frame, orient="vertical", command=course_canvas.yview)
course_list_frame = tk.Frame(course_canvas)

def on_frame_configure(event):
    course_canvas.configure(scrollregion=course_canvas.bbox("all"))

course_list_frame.bind("<Configure>", on_frame_configure)
course_canvas.create_window((0, 0), window=course_list_frame, anchor="nw")
course_canvas.configure(yscrollcommand=course_scrollbar.set)

course_canvas.grid(row=0, column=0, sticky="ns")
course_scrollbar.grid(row=0, column=1, sticky="ns")

overview_title = tk.Label(course_list_frame, text="Course List", font=("Arial", 16, "bold"))
overview_title.grid(row=0, column=0, sticky="ew", pady=(0, 10))

course_widgets = []
for i, (title, desc, url) in enumerate(courses):
    widget = tk.Text(
        course_list_frame,
        height=2,
        width=35,
        font=("Arial", 12),
        padx=5,
        pady=4,
        wrap="word",
        relief="ridge",
        bd=1,
        bg="#f0f0f0",
        cursor="hand2"
    )
    widget.grid(row=i+1, column=0, sticky="ew", pady=2)
    widget.bind("<Button-1>", lambda e, idx=i: on_course_click(e, idx))
    widget.config(state="disabled")
    course_widgets.append(widget)

# Right: Course Details and Navigation (responsive)
details_frame = tk.Frame(main_frame)
details_frame.grid(row=0, column=1, sticky="nsew")
for r in range(7):
    details_frame.grid_rowconfigure(r, weight=0)
details_frame.grid_rowconfigure(5, weight=1)  # Make notes_text row expandable
details_frame.grid_columnconfigure(0, weight=1)
details_frame.grid_columnconfigure(1, weight=0)  # For scrollbar

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(details_frame, variable=progress_var, maximum=len(courses), length=400)
progress_bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(5, 15))

label_title = tk.Label(details_frame, text="Click to begin!", font=("Arial", 16))
label_title.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 10))

label_desc = tk.Label(details_frame, text="", wraplength=500, font=("Arial", 12), justify="left")
label_desc.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

button_next = tk.Button(details_frame, text="", command=open_next, font=("Arial", 14), width=20, height=2)
button_next.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

notes_label = tk.Label(details_frame, text="Your Notes:", font=("Arial", 12))
notes_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=(5, 0))

# Notes text area with dynamic scrollbar
notes_text = tk.Text(
    details_frame,
    height=6,
    width=50,
    font=("Arial", 12),
    wrap=tk.WORD
)
notes_text.grid(row=5, column=0, sticky="nsew", pady=(0, 10))
notes_text.bind("<KeyRelease>", save_note)
notes_text.bind("<<Modified>>", save_note)
notes_text.bind("<Configure>", check_notes_scrollbar)

notes_scrollbar = tk.Scrollbar(details_frame, orient="vertical", command=notes_text.yview)
notes_text.config(yscrollcommand=notes_scrollbar.set)

restart_button = tk.Button(details_frame, text="Restart", command=restart, font=("Arial", 12), width=10)
restart_button.grid(row=6, column=0, columnspan=2, sticky="ew")

update_display()
root.mainloop()
