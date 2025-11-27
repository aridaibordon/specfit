import tkinter as tk

from typing import Dict

from models import FrameConfig
from ui.frames.search import SearchFrame

FRAMES_DICT: Dict[str, FrameConfig] = {
    "search": lambda parent: SearchFrame(parent),
    "test": lambda parent: tk.Label(parent, bg="red"),
    # "fit2": lambda parent: tk.Label(parent, bg="green")
}