from tkinter import ttk
from WorkoutDisplaySegments import WorkoutDisplaySegments

class NotebookWorkoutSegments:
    def __init__(self, root):
        self.__frame = ttk.Frame(root)
        self.__details = WorkoutDisplaySegments(self.__frame)

    def get_notebook(self):
        return self.__frame
    
    def set_workout(self, workout, ftp, min_watt):
        self.__details.set_workout(workout, ftp)