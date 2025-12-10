import tkinter as tk

from typing import Dict

from models import FrameConfig
from ui.frames.fit import FitFrame
from ui.frames.search import SearchFrame

from test.multizone import TestMultizoneFrame


FRAMES_DICT: Dict[str, FrameConfig] = {
    "fit": lambda parent: FitFrame(parent),
    "search": lambda parent: SearchFrame(parent),
    "multizone": lambda parent: TestMultizoneFrame(parent),
    "test": lambda parent: tk.Label(parent, bg="red"),
    # "fit2": lambda parent: tk.Label(parent, bg="green")
}
