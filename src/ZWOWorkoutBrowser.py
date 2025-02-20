import tkinter as tk
from MainDialog import MainDialog

def main():
    root = tk.Tk()
    app = MainDialog(root)
    root.mainloop()

if __name__ == "__main__":
    main()