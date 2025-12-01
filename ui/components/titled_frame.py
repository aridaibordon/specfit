import customtkinter as ctk


class TitledFrame(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, title: str):
        super().__init__(parent, fg_color="transparent")

        frame_label = ctk.CTkLabel(self, text=title)
        frame_label.pack(expand=True, fill="x")

        self.container = ctk.CTkFrame(self)
        self.container.pack(expand=True, fill="both", padx=20, pady=10)
