from tkinter import ttk
from WorkoutDisplayGraph import WorkoutDisplayGraph

class NotebookWorkoutGraph:
    def __init__(self, root):
        self.__frame = ttk.Frame(root)
        self.__details = WorkoutDisplayGraph(self.__frame)

    def get_notebook(self):
        return self.__frame
        
    def set_workout(self, workout):
        self.__details.set_workout(workout)