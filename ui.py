"""
Floating caption window using tkinter.
"""
import tkinter as tk
from collections import deque

MAX_LINES = 4
BG_COLOR = "#1a1a1a"
FG_COLOR = "#ffffff"
FONT = ("PingFang SC", 18)
WINDOW_WIDTH = 760
WINDOW_HEIGHT = 220


class CaptionWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Live Caption")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+100+800")
        self.root.configure(bg=BG_COLOR)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.88)
        self.root.resizable(True, True)

        # Make window draggable
        self._drag_x = 0
        self._drag_y = 0
        self.root.bind("<ButtonPress-1>", self._start_drag)
        self.root.bind("<B1-Motion>", self._drag)

        # Quit on Cmd+Q or Q
        self.root.bind("<Command-q>", lambda e: self.root.quit())
        self.root.bind("<q>", lambda e: self.root.quit())

        self._lines = deque(maxlen=MAX_LINES)

        self.label = tk.Label(
            self.root,
            text="🎙️ 等待日语输入...",
            bg=BG_COLOR,
            fg=FG_COLOR,
            font=FONT,
            wraplength=WINDOW_WIDTH - 40,
            justify="left",
            anchor="nw",
            padx=20,
            pady=16,
        )
        self.label.pack(fill="both", expand=True)

    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _drag(self, event):
        x = self.root.winfo_x() + event.x - self._drag_x
        y = self.root.winfo_y() + event.y - self._drag_y
        self.root.geometry(f"+{x}+{y}")

    def add_line(self, text: str):
        """Thread-safe: schedule UI update from main thread."""
        self.root.after(0, self._update_label, text)

    def _update_label(self, text: str):
        self._lines.append(text)
        display = "\n".join(self._lines)
        self.label.config(text=display)

    def run(self):
        self.root.mainloop()
