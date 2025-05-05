import tkinter as tk
from MainDialog import MainDialog
from tkinter import messagebox
from Options import Options

def on_closing():
    # Optional: Bestätigungsdialog anzeigen
    if messagebox.askokcancel(_("Beenden"), 
                              _("Möchten Sie die Anwendung wirklich schließen?")):
        Options.get_instanz().save_to_file()
        root.destroy()  # Fenster schließen
    
def main():
    global root
    root = tk.Tk()
    Options.get_instanz().set_root(root)  # Set the root window in Options instance
    # Protocol für das Schließen-Ereignis festlegen (WM_DELETE_WINDOW)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app = MainDialog(root)
    root.mainloop()

if __name__ == "__main__":
    main()