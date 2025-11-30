import tkinter as tk

from typing import Dict

from models import FrameConfig
from ui.frames.fit import FitFrame

from test.fit import TestFitFrame
from test.search import TestSearchFrame
from test.multizone import TestMultizoneFrame


FRAMES_DICT: Dict[str, FrameConfig] = {
    "fit": lambda parent: TestFitFrame(parent),
    "search": lambda parent: TestSearchFrame(parent),
    "multizone": lambda parent: TestMultizoneFrame(parent),
    "test": lambda parent: tk.Label(parent, bg="red"),
    # "fit2": lambda parent: tk.Label(parent, bg="green")
}
