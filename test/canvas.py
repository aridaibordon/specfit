import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class SearchFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        fig, ax = plt.subplots(figsize=(4, 3), tight_layout=True)
        ax.plot([1, 2, 3], [1, 4, 9])

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack(fill="none", expand=False, anchor="nw")

root = tk.Tk()

frame = SearchFrame(root)
frame.pack(fill="none", expand=False)   # ← IMPORTANT

root.mainloop()