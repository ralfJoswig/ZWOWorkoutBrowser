import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
from NormalizedAndAveragePower import NormalizedAndAveragePower

class WorkoutDisplayDetails:
    def __init__(self, root):
        self.__frame= tk.Frame(root)
        self.add_fields()
        self.__frame.pack(fill=tk.BOTH, expand=True)

    def get_frame(self):
        return self.__frame
    
    def add_fields(self):
        self.add_name()
        self.add_author()
        self.add_type()
        self.add_segment_count()
        self.add_duration()
        self.add_description()
        self.add_average_power()
        self.add_normalized_power()
        self.add_tss()
        
    def add_tss(self):
        ttk.Label(self.__frame, 
                  text="TSS:").grid(row=2, 
                                   column=2, 
                                   sticky='w', 
                                   padx=10, 
                                   pady=5)
        self.__tss_var = tk.StringVar(value="")
        self.__tss_entry = ttk.Entry(self.__frame, 
                                     textvariable=self.__tss_var, 
                                     width=5, 
                                     state="readonly")
        self.__tss_entry.grid(row=2, 
                              column=3, 
                              sticky='w', 
                              padx=10, 
                              pady=5)

    def add_normalized_power(self):
        ttk.Label(self.__frame, 
                  text="NP:").grid(row=2, 
                                   column=0, 
                                   sticky='w', 
                                   padx=10, 
                                   pady=5)
        self.__normalized_power_var = tk.StringVar(value="")
        self.__normalized_power_entry = ttk.Entry(self.__frame, 
                                                textvariable=self.__normalized_power_var, 
                                                width=5, 
                                                state="readonly")
        self.__normalized_power_entry.grid(row=2, 
                                           column=1, 
                                           sticky='w', 
                                           padx=10, 
                                           pady=5)
        
    def add_average_power(self):
        ttk.Label(self.__frame, 
                  text="Durchschnittsleistung:").grid(row=1, 
                                                      column=4, 
                                                      sticky='w', 
                                                      padx=10, 
                                                      pady=5)
        self.__avg_power_var = tk.StringVar(value="")
        self.__avg_power_entry = ttk.Entry(self.__frame, 
                                           textvariable=self.__avg_power_var, 
                                           width=5, 
                                           state="readonly")
        self.__avg_power_entry.grid(row=1, 
                                    column=5, 
                                    sticky='w', 
                                    padx=10, 
                                    pady=5)
        
    def add_description(self):
        ttk.Label(self.__frame, 
                  text="Bemerkung:").grid(row=3, 
                                          column=0, 
                                          columnspan=2, 
                                          sticky='w', 
                                          padx=10, 
                                          pady=5)
        # Frame für Bemerkungstext und Scrollbar
        remark_frame = ttk.Frame(self.__frame)
        remark_frame.grid(row=4, 
                          column=0, 
                          columnspan=6, 
                          padx=50, 
                          pady=5, 
                          sticky='nsew')
        
        # Konfiguriere Grid für den Remark Frame
        remark_frame.grid_rowconfigure(0, 
                                       weight=1)
        remark_frame.grid_columnconfigure(0, 
                                          weight=1)
        
        self.remark_text = tk.Text(remark_frame, 
                                   height=10, 
                                   width=50, 
                                   wrap=tk.WORD, 
                                   state=tk.DISABLED)
        self.remark_text.grid(row=0, 
                              column=0, 
                              sticky='nsew')
        
        scrollbar = ttk.Scrollbar(remark_frame, 
                                  command=self.remark_text.yview)
        scrollbar.grid(row=0, 
                       column=1, 
                       sticky='ns')
        self.remark_text.config(yscrollcommand=scrollbar.set)

    def add_name(self):
        ttk.Label(self.__frame, 
                  text="Name:").grid(row=0, 
                                     column=0, 
                                     sticky='w', 
                                     padx=10, 
                                     pady=5)
        self.__name_var = tk.StringVar(value="")
        self.__name_entry = ttk.Entry(self.__frame, 
                                      textvariable=self.__name_var, 
                                      width=30, 
                                      state="readonly")
        self.__name_entry.grid(row=0, 
                               column=1, 
                               sticky='w', 
                               padx=10, 
                               pady=5)

    def add_author(self):
        ttk.Label(self.__frame, 
                  text="Autor:").grid(row=0, 
                                      column=2, 
                                      sticky='w', 
                                      padx=10, 
                                      pady=5)
        self.__author_var = tk.StringVar(value="")
        self.__author_entry = ttk.Entry(self.__frame, 
                                        textvariable=self.__author_var, 
                                        width=30, 
                                        state="readonly")
        self.__author_entry.grid(row=0, 
                                 column=3, 
                                 sticky='w', 
                                 padx=10, 
                                 pady=5)

    def add_type(self):
        ttk.Label(self.__frame, 
                  text="Typ:").grid(row=0, 
                                    column=4, 
                                    sticky='w', 
                                    padx=10, 
                                    pady=5)
        self.__type_var = tk.StringVar(value="")
        self.__type_entry = ttk.Entry(self.__frame, 
                                      textvariable=self.__type_var, 
                                      width=20, 
                                      state="readonly")
        self.__type_entry.grid(row=0, 
                               column=5, 
                               sticky='w', 
                               padx=10, 
                               pady=5)
        
    def add_segment_count(self):
        ttk.Label(self.__frame, 
                  text="Anzahl Segmente:").grid(row=1, 
                                                column=0, 
                                                sticky='w', 
                                                padx=10, 
                                                pady=5)
        self.__seg_count_var = tk.StringVar(value="")
        self.__seg_count_entry = ttk.Entry(self.__frame, 
                                           textvariable=self.__seg_count_var, 
                                           width=5, 
                                           state="readonly")
        self.__seg_count_entry.grid(row=1, 
                                    column=1, 
                                    sticky='w', 
                                    padx=10, 
                                    pady=5)
        
    def add_duration(self):
        ttk.Label(self.__frame, 
                  text="Dauer:").grid(row=1, 
                                      column=2, 
                                      sticky='w', 
                                      padx=10, 
                                      pady=5)
        self.__duration_var = tk.StringVar(value="")
        self.__duration_entry = ttk.Entry(self.__frame, 
                                          textvariable=self.__duration_var, 
                                          width=10, 
                                          state="readonly")
        self.__duration_entry.grid(row=1, 
                                   column=3, 
                                   sticky='w', 
                                   padx=10, 
                                   pady=5)
        
    def set_description(self, description):       
        self.remark_text.config(state=tk.NORMAL)
        self.remark_text.delete(1.0, 
                                tk.END)
        self.remark_text.insert(tk.END, 
                                description if description != None else "")
        self.remark_text.config(state=tk.DISABLED)

    def set_workout(self, workout, ftp):
        self.__name_var.set(workout.name)
        self.__author_var.set(workout.author)
        self.__type_var.set(workout.sportType.value)
        self.__seg_count_var.set(len(workout.segments))
        self.__duration_var.set(workout.get_duration_as_text())
        self.set_description(workout.description)

        normalized_power, average_power = NormalizedAndAveragePower(workout).calculate(ftp)
        self.__avg_power_var.set(average_power)
        self.__normalized_power_var.set(normalized_power)
        
        intensitaetsfaktor = normalized_power / ftp
        tss = round(( workout.duration * normalized_power * intensitaetsfaktor ) / ( ftp * 3600 ) * 100)
        self.__tss_var.set(tss)