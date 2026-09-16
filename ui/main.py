import customtkinter as ctk
import tkinter as tk

import config

import ui.frames as frames

DEFAULT_FRAME = "fit"


class MainFrame(ctk.CTkFrame):
    def __init__(self, root: ctk.CTk):
        super().__init__(root)

        # app menu
        main_menu = tk.Menu(root)
        config_menu = tk.Menu(main_menu, tearoff=0)
        config_menu.add_command(label="Select database", command=self.select_database)

        main_menu.add_cascade(label="Config", menu=config_menu)

        root.config(menu=main_menu)

        # navegation menu
        navegation_menu = ctk.CTkFrame(self, fg_color="transparent")

        navegation_buttons = [
            ctk.CTkButton(
                navegation_menu,
                text="Searching tools",
                command=lambda: self.update_main_frame("search"),
            ),
            ctk.CTkButton(
                navegation_menu,
                text="Manual fitting",
                command=lambda: self.update_main_frame("fit"),
            ),
            ctk.CTkButton(
                navegation_menu,
                text="Configuration",
                command=lambda: self.update_main_frame("config"),
            ),
        ]
        for button in navegation_buttons:
            button.pack(fill="x", padx=5, pady=2, ipadx=10, ipady=2)

        # main frame
        self.main_frame = frames.FRAMES_DICT[DEFAULT_FRAME](self)
        self.current_frame = DEFAULT_FRAME

        # layout
        self.grid_columnconfigure(0, minsize=200, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        navegation_menu.grid(column=0, row=0, sticky="ns", padx=20, pady=10)
        self.main_frame.grid(column=1, row=0, sticky="nwse", padx=20, pady=10)

    def select_database(self) -> None:
        db_path = ctk.filedialog.askdirectory()
        if not db_path or db_path == config.read_entry("db"):
            return

        config.add_entry("db", db_path)
        self.update_main_frame(self.current_frame, redraw=True)

    def update_main_frame(self, next, redraw=False) -> None:
        if (self.current_frame == next) and not redraw:
            return

        self.main_frame.destroy()

        self.main_frame: ctk.CTkFrame = frames.FRAMES_DICT[next](self)
        self.main_frame.grid(column=1, row=0, sticky="nwse", padx=20, pady=10)

        self.current_frame = next
