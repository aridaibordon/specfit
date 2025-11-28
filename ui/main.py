import tkinter as tk

from tkinter import ttk

from ui.frames import FRAMES_DICT


DEFAULT_FRAME = "search"


class AppMenu(tk.Menu):
    def __init__(self, root):
        super().__init__(root)
        config_menu = tk.Menu(self)

        config_menu.add_cascade(label="Config", menu=self)
        config_menu.add_command(label="Select database")
        config_menu.add_command(label="Select sample")


class MainFrame(tk.Frame):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        # App menu
        main_menu = AppMenu(root)
        root.config(menu=main_menu)

        # Navegation menu
        navegation_menu = tk.Frame(self)

        navegation_container = tk.Frame(navegation_menu)
        navegation_container.pack(padx=10, pady=10, expand=True, fill="both")

        navegation_buttons = [
            ttk.Button(
                navegation_container,
                text="Signal postprocessing",
                command=lambda: self.change_main_frame("test"),
            ),
            ttk.Button(
                navegation_container,
                text="Searching tools",
                command=lambda: self.change_main_frame("search"),
            ),
            ttk.Button(
                navegation_container,
                text="Manual fitting",
                command=lambda: self.change_main_frame("fit"),
            ),
        ]
        for button in navegation_buttons:
            button.pack(fill="x")
        
        # Main frame
        self.main_container = tk.Frame(self)

        self.main_frame = FRAMES_DICT[DEFAULT_FRAME](self.main_container)
        self.main_frame.pack(padx=10, pady=10, expand=True, fill="both")

        self.current_frame = DEFAULT_FRAME

        # LAYOUT
        self.grid_columnconfigure(0, minsize=200, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        navegation_menu.grid(column=0, row=0, sticky="n")
        self.main_container.grid(column=1, row=0, sticky="nwse")


    def change_main_frame(self, next) -> None:
        if self.current_frame == next:
            return

        self.main_frame.destroy()

        self.main_frame: tk.Frame = FRAMES_DICT[next](self.main_container)
        self.main_frame.pack(padx=10, pady=10, expand=True, fill="both")

        self.current_frame = next
