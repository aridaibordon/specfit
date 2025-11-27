import tkinter as tk

from typing import Dict

from models import FrameConfig
from ui.frames.fit import FitFrame

FRAMES_DICT: Dict[str, FrameConfig] = {
    "fit": lambda parent: FitFrame(parent),
    "search": lambda parent: FitFrame(parent),
    "test": lambda parent: tk.Label(parent, bg="red"),
    # "fit2": lambda parent: tk.Label(parent, bg="green")
}