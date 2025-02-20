import tkinter as tk
from tkinter import ttk

class WorkoutDisplaySegments:
    def __init__(self, root):
        self.__frame= tk.Frame(root)
        self.add_workout_table()
        self.__frame.pack(fill=tk.BOTH, expand=True)

    def get_frame(self):
        return self.__frame
    
    def add_workout_table(self):
        self.__tree = ttk.Treeview(self.__frame, 
                                   show='headings')
        self.__tree["columns"] = ("Wiederholungen",
                                  "Dauer", 
                                  "Typ", 
                                  "Watt", 
                                  "Cadence",
                                  "Texte")
        
        self.__tree.heading("Wiederholungen",
                            text="Wiedh.")
        self.__tree.heading("Dauer", 
                            text="Dauer")
        self.__tree.heading("Typ", 
                            text="Typ")
        self.__tree.heading("Watt", 
                            text="Watt")
        self.__tree.heading("Cadence", 
                            text="Cadence")
        self.__tree.heading("Texte", 
                            text="Texte")
        
        self.__tree.column("Wiederholungen",
                            width=50)
        self.__tree.column("Dauer", 
                           width=50)
        self.__tree.column("Typ", 
                           width=90)
        self.__tree.column("Watt", 
                            width=50)
        self.__tree.column("Cadence", 
                           width=50)
        self.__tree.column("Texte", 
                           width=50)

        self.__tree.pack(fill=tk.BOTH, 
                         expand=True)

    def tree_delete(self):
        self.__tree.delete(*self.__tree.get_children())
        
    def tree_insert(self, segment, power):
        self.__tree.insert("", 
                           "end", 
                           values=(segment.get_repeat() if hasattr(segment, 'get_repeat') else "",
                                   segment.get_duration_as_text(),
                                   segment.get_segment_type().value,
                                   power,
                                   segment.get_cadence(),
                                   segment.get_text_count()))

    def set_workout(self, workout, ftp):
        self.tree_delete()
        
        for segment in workout.segments:
            self.tree_insert(segment, segment.get_power().get_as_text(ftp))