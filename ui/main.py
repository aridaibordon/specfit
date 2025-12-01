import customtkinter as ctk
import tkinter as tk

import ui.frames as frames


DEFAULT_FRAME = "search"


class AppMenu(tk.Menu):
    def __init__(self, root):
        super().__init__(root)
        config_menu = tk.Menu(self)
        config_menu.add_command(label="Select database")
        config_menu.add_command(label="Select sample")

        self.add_cascade(label="Config", menu=config_menu)


class MainFrame(ctk.CTkFrame):
    def __init__(self, root: ctk.CTk):
        super().__init__(root)

        # App menu
        main_menu = AppMenu(root)
        root.config(menu=main_menu)

        # Navegation menu
        navegation_menu = ctk.CTkFrame(self, fg_color="transparent")

        navegation_buttons = [
            # ctk.CTkButton(
            #     navegation_menu,
            #     text="Signal postprocessing",
            #     command=lambda: self.change_main_frame("test"),
            # ),
            ctk.CTkButton(
                navegation_menu,
                text="Searching tools",
                command=lambda: self.change_main_frame("search"),
            ),
            # ctk.CTkButton(
            #     navegation_container,
            #     text="Searching tools (mz)",
            #     command=lambda: self.change_main_frame("multizone"),
            # ),
            ctk.CTkButton(
                navegation_menu,
                text="Manual fitting",
                command=lambda: self.change_main_frame("fit"),
            ),
            ctk.CTkButton(
                navegation_menu,
                text="Configuration",
                command=lambda: self.change_main_frame("config"),
            ),
        ]
        for button in navegation_buttons:
            button.pack(fill="x", padx=5, pady=2, ipadx=10, ipady=2)

        # Main frame
        self.main_frame = frames.FRAMES_DICT[DEFAULT_FRAME](self)
        self.current_frame = DEFAULT_FRAME

        # LAYOUT
        self.grid_columnconfigure(0, minsize=200, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        navegation_menu.grid(column=0, row=0, sticky="n", padx=10, pady=10)
        self.main_frame.grid(column=1, row=0, sticky="nwse", padx=10, pady=10)

    def change_main_frame(self, next) -> None:
        if self.current_frame == next:
            return

        self.main_frame.destroy()

        self.main_frame: ctk.CTkFrame = frames.FRAMES_DICT[next](self)
        self.main_frame.grid(column=1, row=0, sticky="nwse", padx=0, pady=10)

        self.current_frame = next
