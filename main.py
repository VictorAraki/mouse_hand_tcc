import tkinter as tk 

from interface import MouseControlInterface


if __name__ == "__main__":
    root = tk.Tk()
    app = MouseControlInterface(root)
    root.mainloop()