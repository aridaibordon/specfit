import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class App(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Make this frame expand
        self.grid(row=0, column=0, sticky="nsew")
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)

        # ------------------------------
        # Create figure + canvas
        # ------------------------------
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot([1, 2, 3], [1, 4, 9])

        canvas = FigureCanvasTkAgg(fig, self)
        canvas_widget = canvas.get_tk_widget()

        # Place canvas with grid
        canvas_widget.grid(row=0, column=0, sticky="nsew")

        # Make the canvas cell expandable
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Add a simple widget for comparison
        button = ttk.Button(self, text="Redraw", command=canvas.draw)
        button.grid(row=1, column=0, pady=10)


root = tk.Tk()
root.geometry("600x500")

app = App(root)
root.mainloop()
