import GraphicsParameter
import tkinter as tk

from pathlib import Path
import gettext

class CoordinateSystem:
    def __init__(self, parameters: GraphicsParameter):
        self.parameters = parameters

        if self.parameters.max_y < self.parameters.min_watt:
            self.max_y = self.parameters.min_watt
        else:
            self.max_y = self.parameters.max_y

    def plot_x_axsis(self):
         # X-Achse
        self.parameters.canvas.create_line(self.parameters.rand, 
                                           self.parameters.hoehe + self.parameters.rand, 
                                           self.parameters.breite + self.parameters.rand + 10, 
                                           self.parameters.hoehe + self.parameters.rand, 
                                           arrow=tk.LAST)
        
        # Beschriftungen X-Achse (Zeit in Minuten)
        for i in range(0, self.parameters.max_x + 1, 10):
            x = self.parameters.rand + (i * self.parameters.breite / self.parameters.max_x)
            self.parameters.canvas.create_text(x, 
                                               self.parameters.hoehe + self.parameters.rand + 20, 
                                               text=str(i))
            self.parameters.canvas.create_line(x, 
                                               self.parameters.hoehe + self.parameters.rand + 5, 
                                               x, 
                                               self.parameters.hoehe + self.parameters.rand - 5)
            
        # Achsenbeschriftungen
        self.parameters.canvas.create_text(self.parameters.breite/2 + self.parameters.rand, 
                                self.parameters.hoehe + self.parameters.rand + 40, 
                                text=_("Zeit (Minuten)"))

    def plot_y_axsis(self):
        # Y-Achse
        self.parameters.canvas.create_line(self.parameters.rand, 
                                           self.parameters.hoehe + self.parameters.rand, 
                                           self.parameters.rand, 
                                           self.parameters.rand, 
                                           arrow=tk.LAST)
        
        # Beschriftungen Y-Achse (Watt)
        for i in range(0, self.max_y, 20):
            y = self.parameters.hoehe + self.parameters.rand - (i * self.parameters.hoehe / self.max_y)
            self.parameters.canvas.create_text(self.parameters.rand - 20, 
                                               y, 
                                               text=str(i))
            self.parameters.canvas.create_line(self.parameters.rand - 5, 
                                               y, 
                                               self.parameters.rand + 5, 
                                               y)
            
        self.parameters.canvas.create_text(self.parameters.rand - 40, 
                                           self.parameters.hoehe/2, 
                                           text="Watt", 
                                           angle=90)
        
    def plot_z_axsis(self):
        # Z-Achse
        self.parameters.canvas.create_line(self.parameters.breite + self.parameters.rand + 10, 
                                           self.parameters.hoehe + self.parameters.rand, 
                                           self.parameters.rand + self.parameters.breite + 10, 
                                           self.parameters.rand, 
                                           arrow=tk.LAST)
        
        # Beschriftungen Z-Achse (Cadence)
        for i in range(0, self.parameters.max_cadence, 10):
            y = self.parameters.hoehe + self.parameters.rand - (i * self.parameters.hoehe / self.parameters.max_cadence)
            self.parameters.canvas.create_text(self.parameters.rand + self.parameters.breite + 25, 
                                               y, 
                                               text=str(i))
            self.parameters.canvas.create_line(self.parameters.rand + self.parameters.breite + 10 - 5, 
                                               y, 
                                               self.parameters.rand + self.parameters.breite + 10 + 5, 
                                               y)
            
        self.parameters.canvas.create_text(self.parameters.rand + self.parameters.breite + 40,
                                           self.parameters.hoehe / 2,
                                           text=_("Cadence"),
                                           angle=270)
            
    def plot_ftp_line(self):
        #Line für FTP
        y1 = self.parameters.hoehe + self.parameters.rand - (self.parameters.ftp * self.parameters.hoehe / self.parameters.max_y)
        self.parameters.canvas.create_line(self.parameters.rand, 
                                           y1, 
                                           self.parameters.breite + self.parameters.rand, 
                                           y1,
                                           width=3,
                                           fill="cyan")
        
        self.parameters.canvas.create_text(self.parameters.rand + self.parameters.breite + 40,
                                           y1,#self.parameters.hoehe / 2,
                                           text=_("FTP"),
                                           angle=270,
                                           fill="cyan")
        
    def plot(self):
        self.plot_x_axsis()
        self.plot_y_axsis()
        self.plot_z_axsis()
        self.plot_ftp_line() 