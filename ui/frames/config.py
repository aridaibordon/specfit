import tkinter as tk

from tkinter import filedialog, ttk

import config


def select_database():
    db_dialog = filedialog.askdirectory(title="Select spectral database folder")
    if not db_dialog:
        return

    config.add_entry("db", db_dialog)