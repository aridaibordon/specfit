import logging
import tkinter as tk

from ui.main import MainFrame

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SpecFit: a graphical interface for plasma characterization")
        self.geometry("800x600")
        self.minsize(900, 600)

        main_window = MainFrame(self)
        main_window.pack(fill="both", expand=True)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
