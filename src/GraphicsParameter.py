from dataclasses import dataclass
import tkinter as tk

@dataclass
class GraphicsParameter:
    canvas : tk.Canvas
    rand : int
    hoehe : int
    breite : int
    y0 : int
    x0 : int
    _max_y : int = 0
    _min_watt : int = 0
    max_x : int = 0
    max_cadence : int = 0
    ftp : int = 0
    
    @property
    def max_y(self):
        return self._max_y
    
    @max_y.setter
    def max_y(self, value):
        if value < self._min_watt:
            self._max_y = self._min_watt
        else:
            self._max_y = value
            
    @property
    def min_watt(self):
        return self._min_watt
    
    @min_watt.setter
    def min_watt(self, value):
        self._min_watt = value
        if self._max_y < value:
            self._max_y = value