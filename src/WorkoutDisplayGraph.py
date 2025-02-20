import tkinter as tk
from EnumSegmentType import SegmentType

class WorkoutDisplayGraph:
    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, 
                        expand=True)
        self.workout = None
        self.ftp = None
        self.draw_first_cadence = True
        self.min_watt = 0
        self.max_x = 0
        self.max_y = 0
        # Canvas erstellen mit weißem Hintergrund
        self.window_width = 800
        self.window_height = 600
        self.canvas = tk.Canvas(root, 
                                width=self.window_width, 
                                height=self.window_height, 
                                bg='white')
        self.canvas.pack(fill=tk.BOTH, 
                         expand=True, 
                         padx=20, 
                         pady=20)
        
        # Konstanten für die Darstellung
        self.rand = 50  # Rand um das Koordinatensystem
        self.breite = self.window_width - 100 # Nutzbare Breite
        self.hoehe = self.window_height - 100 # Nutzbare Höhe

        self.x0 = self.rand
        self.y0 = self.hoehe + self.rand

        self.tooltip_position_offset = 30

        # Tooltip-Label erstellen (anfangs unsichtbar)
        self.tooltip = tk.Label(root,
                                bg='lightyellow',
                                relief='solid',
                                borderwidth=1)

        self.bind_events()

        self.segment_clicked = False

        self.last_cadence_y = 0

    def on_resize(self, event):
        if self.workout and self.ftp:
            self.window_width = max(event.width, 100)
            self.window_height = max(event.height, 100)
            self.breite = self.window_width - 100
            self.hoehe = self.window_height - 100
            self.x0 = self.rand
            self.y0 = self.hoehe + self.rand
            self.hide_tooltip(None)
            self.set_workout(self.workout, self.ftp, self.min_watt)

    def bind_events(self):
        self.canvas.tag_bind('segment', 
                             '<Button-1>', 
                             self.on_click)
        self.canvas.bind('<Button-1>', 
                         self.hide_tooltip)
        self.canvas.bind('<Configure>', 
                         self.on_resize)

    def on_click(self, event):
        # Finde das Polygon unter dem Mauszeiger
        item = self.canvas.find_closest(event.x, 
                                        event.y)
        # Hole alle Tags des Polygons
        tags = self.canvas.gettags(item)
        # Formatiere die Tags für die Anzeige
        tags_text = ""
        for tag in tags:
            if tag != 'segment' and tag != 'current':
                tags_text += tag + "\n"
        
        # Tooltip konfigurieren und anzeigen
        self.tooltip.config(text=tags_text)
        self.update_tooltip_position(event)
        self.tooltip.lift()
        self.tooltip.place_configure(x=event.x + self.tooltip_position_offset, 
                                     y=event.y + self.tooltip_position_offset)
        self.segment_clicked = True

    def hide_tooltip(self, event):
        # Tooltip ausblenden
        if not self.segment_clicked:
            self.tooltip.place_forget()
        self.segment_clicked = False
    
    def update_tooltip_position(self, event):
        # Tooltip-Position an Mausposition anpassen
        if self.tooltip.winfo_viewable():
            self.tooltip.place_configure(x=event.x + self.tooltip_position_offset, 
                                         y=event.y + self.tooltip_position_offset)

    def zeichne_koordinatensystem(self, max_cadence):
        # X-Achse
        self.canvas.create_line(self.rand, 
                                self.hoehe + self.rand, 
                                self.breite + self.rand + 10, 
                                self.hoehe + self.rand, 
                                arrow=tk.LAST)
        
        # Y-Achse
        self.canvas.create_line(self.rand, 
                                self.hoehe + self.rand, 
                                self.rand, 
                                self.rand, 
                                arrow=tk.LAST)
        
        # Z-Achse
        self.canvas.create_line(self.breite + self.rand + 10, 
                                self.hoehe + self.rand, 
                                self.rand + self.breite + 10, 
                                self.rand, 
                                arrow=tk.LAST)

        
        # Beschriftungen X-Achse (Zeit in Minuten)
        for i in range(0, self.max_x + 1, 10):
            x = self.rand + (i * self.breite / self.max_x)
            self.canvas.create_text(x, 
                                    self.hoehe + self.rand + 20, 
                                    text=str(i))
            self.canvas.create_line(x, 
                                    self.hoehe + self.rand + 5, 
                                    x, 
                                    self.hoehe + self.rand - 5)
        
        # Beschriftungen Y-Achse (Watt)
        if self.max_y < self.min_watt:
            max_y = self.min_watt
        else:
            max_y = self.max_y

        for i in range(0, max_y, 20):
            y = self.hoehe + self.rand - (i * self.hoehe / max_y)
            self.canvas.create_text(self.rand - 20, 
                                    y, 
                                    text=str(i))
            self.canvas.create_line(self.rand - 5, 
                                    y, 
                                    self.rand + 5, 
                                    y)
        
        # Beschriftungen Z-Achse (Cadence)
        for i in range(0, max_cadence, 10):
            y = self.hoehe + self.rand - (i * self.hoehe / max_cadence)
            self.canvas.create_text(self.rand + self.breite + 25, 
                                    y, 
                                    text=str(i))
            self.canvas.create_line(self.rand + self.breite + 10 - 5, 
                                    y, 
                                    self.rand + self.breite + 10 + 5, 
                                    y)
            
        # Achsenbeschriftungen
        self.canvas.create_text(self.breite/2 + self.rand, 
                                self.hoehe + self.rand + 40, 
                                text="Zeit (Minuten)")
        self.canvas.create_text(self.rand - 40, 
                                self.hoehe/2, 
                                text="Watt", 
                                angle=90)
        self.canvas.create_text(self.rand + self.breite + 40,
                                self.hoehe / 2,
                                text="Cadence",
                                angle=270)
        
        #Line für FTP
        if self.max_y < self.min_watt:
            max_y = self.min_watt
        else:
            max_y = self.max_y

        y1 = self.hoehe + self.rand - (self.ftp * self.hoehe / max_y)
        self.canvas.create_line(self.rand, 
                                y1, 
                                self.breite + self.rand, 
                                y1,
                                width=3,
                                fill="cyan") 
        
    def det_fill_colour(self, power):
        ftp_proz = 100 * power / self.ftp if self.ftp != 0 else 100
        if ftp_proz < 55:
            return 'gray'
        elif ftp_proz < 75:
            return 'blue'
        elif ftp_proz < 90:
            return 'green'
        elif ftp_proz < 105:
            return 'dark green'
        elif ftp_proz < 120:
            return 'yellow'
        elif ftp_proz < 150:
            return 'orange'
        else:
            return 'red'

    def zeichne_segment(self, min_power, max_power, duration, tags, cadence, max_cadence):
        # Polygon zeichnen
        # Die Koordinaten werden als Liste von x,y Punkten übergeben
        # Format: [x1, y1, x2, y2, x3, y3, ...]
        if self.max_y < self.min_watt:
            max_y = self.min_watt
        else:
            max_y = self.max_y

        y1 = self.hoehe + self.rand - (min_power * self.hoehe / max_y)
        y2 = self.hoehe + self.rand - (max_power * self.hoehe / max_y)
        x2 = self.last_x + (duration * self.breite / self.max_x) 
        polygon_coords = [self.last_x, 
                          self.y0,
                          self.last_x, 
                          y1,
                          x2, 
                          y2, 
                          x2, 
                          self.y0]
        
        fill_colour = self.det_fill_colour(max_power)

        tags.insert(0, 'segment')
        self.canvas.create_polygon(polygon_coords,
                                   fill=fill_colour,        # Füllfarbe
                                   outline='red',    # Randfarbe
                                   width=1,
                                   tags=tags)
        
        if max_cadence != 0 and cadence != 0:
            y1 = self.hoehe + self.rand - (cadence * self.hoehe / max_cadence)
            y2 = y1
            if self.draw_first_cadence == False:
                self.canvas.create_line(self.last_x,
                                        self.last_cadence_y,
                                        self.last_x,
                                        y1,
                                        fill="yellow",
                                        width=5)
            self.canvas.create_line(self.last_x, 
                                    y1, 
                                    x2, 
                                    y2, 
                                    fill='yellow', 
                                    width=5)
            self.draw_first_cadence = False

        self.last_x = x2
        self.last_cadence_y = y2
        
    def get_frame(self):
        return self.__frame
    
    def set_workout(self, workout, ftp, min_watt):
        self.max_x = int(workout.duration / 60)
        self.max_y = int(workout.max_power * ftp)
        self.canvas.delete('all')
        self.workout = workout
        self.ftp = ftp
        self.draw_first_cadence = True
        self.min_watt = min_watt
        self.zeichne_koordinatensystem(workout.get_max_cadence())
        self.hide_tooltip(None)
        self.last_x = self.x0
        for segment in workout.segments:
            if segment.get_segment_type() == SegmentType.INTERVALST:
                for i in range(segment.get_repeat()):
                    on_power = int(segment.get_power().start_power * ftp)
                    off_power = int(segment.get_power().end_power * ftp)
                    tags = [f"Dauer: {segment.get_on_duration_as_text()}",]
                    tags.append(f"Leistung: {on_power}")
                    if segment.get_cadence() > 0:
                        tags.append(f"Trittfrequenz: {segment.get_cadence()}")
                    self.zeichne_segment(on_power, 
                                         on_power, 
                                         segment.on_duration / 60,tags,
                                         segment.get_cadence(), 
                                         workout.get_max_cadence())
                    tags = [f"Dauer: {segment.get_off_duration_as_text()}",]
                    tags.append(f"Leistung: {off_power}")
                    if segment.get_cadence() > 0:
                        tags.append(f"Trittfrequenz: {segment.get_cadence()}")
                    self.zeichne_segment(off_power, 
                                         off_power, 
                                         segment.off_duration / 60,tags,
                                         segment.get_cadence(), 
                                         workout.get_max_cadence())
            else:
                start_power = int(segment.get_power().start_power * ftp)
                end_power = int(segment.get_power().end_power * ftp)

                tags = [f"Dauer: {segment.get_duration_as_text()}",]
                if segment.get_power().start_power == segment.get_power().end_power:
                    tags.append(f"Leistung: {start_power}")
                else:
                    tags.append(f"Leistung: {start_power}/{end_power}")
                dummy = segment.get_cadence()
                if segment.get_cadence() > 0:
                    tags.append(f"Trittfrequenz: {segment.get_cadence()}")
                
                self.zeichne_segment(start_power,
                                     end_power,  
                                     segment.get_duration() / 60,
                                     tags,
                                     segment.get_cadence(), 
                                     workout.get_max_cadence())
