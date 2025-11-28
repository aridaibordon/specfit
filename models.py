import tkinter as tk

from dataclasses import dataclass
from typing import Tuple


@dataclass
class FrameConfig:
    frame_class: tk.Frame
    description: str
    abbrv: str

    def instanciate(self, parent) -> tk.Frame:
        return lambda parent: self.frame_class(parent)

    def unpack(self) -> Tuple[tk.Frame, str, str]:
        return self.frame_class, self.abbrv, self.description
