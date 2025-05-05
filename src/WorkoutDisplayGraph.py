import tkinter as tk
from EnumSegmentType import SegmentType
import GraphicsParameter
import CoordinateSystem
from Options import Options

class WorkoutDisplayGraph:
    def __init__(self, root):
        window_width = 800
        window_height = 600
        self.workout = None
        self.draw_first_cadence = True
        self.tooltip_position_offset = 30
        self.segment_clicked = False
        self.last_cadence_y = 0
        
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, 
                    expand=True)

        # Tooltip-Label erstellen (anfangs unsichtbar)
        self.tooltip = tk.Label(root,
                                bg='lightyellow',
                                relief='solid',
                                borderwidth=1)

        canvas = tk.Canvas(root, 
                           width=window_width, 
                           height=window_height, 
                           bg='white')
        canvas.pack(fill=tk.BOTH, 
                    expand=True, 
                    padx=20, 
                    pady=20)
        
        rand = 50 # Rand um das Koordinatensystem
        hoehe = window_height - 100 # Nutzbare Höhe
        y0 = rand + hoehe
        self.parameters = GraphicsParameter.GraphicsParameter(canvas = canvas,
                                                              rand = rand,
                                                              hoehe = hoehe,
                                                              breite = window_width - 100, # Nutzbare Breite
                                                              y0 = y0,
                                                              x0 = rand) 
        
        self.bind_events()

    def on_resize(self, event):
        if self.workout and self.parameters.ftp:
            window_width = max(event.width, 100)
            window_height = max(event.height, 100)
            self.parameters.breite = window_width - 100
            self.parameters.hoehe = window_height - 100
            self.parameters.x0 = self.parameters.rand
            self.parameters.y0 = self.parameters.hoehe + self.parameters.rand
            self.hide_tooltip(None)
            self.set_workout(self.workout)

    def bind_events(self):
        self.parameters.canvas.tag_bind('segment', 
                             '<Button-1>', 
                             self.on_click)
        self.parameters.canvas.bind('<Button-1>', 
                         self.hide_tooltip)
        self.parameters.canvas.bind('<Configure>', 
                         self.on_resize)

    def on_click(self, event):
        # Finde das Polygon unter dem Mauszeiger
        item = self.parameters.canvas.find_closest(event.x, 
                                        event.y)
        # Hole alle Tags des Polygons
        tags = self.parameters.canvas.gettags(item)
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
        self.CoordinateSystem = CoordinateSystem.CoordinateSystem(self.parameters)
        self.CoordinateSystem.plot()
        
    def det_fill_colour(self, power):
        ftp_proz = 100 * power / self.parameters.ftp if self.parameters.ftp != 0 else 100
        if ftp_proz < 56:
            return 'gray'
        elif ftp_proz < 76:
            return 'blue'
        elif ftp_proz < 91:
            return 'green'
        elif ftp_proz < 106:
            return 'yellow'
        elif ftp_proz < 121:
            return 'orange'
        elif ftp_proz < 151:
            return 'red'
        else:
            return 'dark red'

    def zeichne_segment(self, min_power, max_power, duration, tags, cadence, max_cadence):
        # Polygon zeichnen
        # Die Koordinaten werden als Liste von x,y Punkten übergeben
        # Format: [x1, y1, x2, y2, x3, y3, ...]
        if self.parameters.max_y < self.parameters.min_watt:
            max_y = self.parameters.min_watt
        else:
            max_y = self.parameters.max_y

        y1 = self.parameters.hoehe + self.parameters.rand - (min_power * self.parameters.hoehe / max_y)
        y2 = self.parameters.hoehe + self.parameters.rand - (max_power * self.parameters.hoehe / max_y)
        x2 = self.last_x + (duration * self.parameters.breite / self.parameters.max_x) 
        polygon_coords = [self.last_x, 
                          self.parameters.y0,
                          self.last_x, 
                          y1,
                          x2, 
                          y2, 
                          x2, 
                          self.parameters.y0]
        
        fill_colour = self.det_fill_colour(max_power)

        tags.insert(0, 'segment')
        self.parameters.canvas.create_polygon(polygon_coords,
                                   fill=fill_colour,        # Füllfarbe
                                   outline='red',    # Randfarbe
                                   width=1,
                                   tags=tags)
            
        if cadence == 0:    
            self.draw_first_cadence = True
            
        if max_cadence != 0 and cadence != 0:
            y1 = self.parameters.hoehe + self.parameters.rand - (cadence * self.parameters.hoehe / max_cadence)
            y2 = y1
            if self.draw_first_cadence == False:
                self.parameters.canvas.create_line(self.last_x,
                                        self.last_cadence_y,
                                        self.last_x,
                                        y1,
                                        fill="navy",
                                        width=5)
            self.parameters.canvas.create_line(self.last_x, 
                                    y1, 
                                    x2, 
                                    y2, 
                                    fill='navy', 
                                    width=5)
            self.draw_first_cadence = False

        self.last_x = x2
        self.last_cadence_y = y2
        
    def get_frame(self):
        return self.__frame
    
    def set_workout(self, workout):
        options = Options.get_instanz()
        ftp = options.get_ftp()
        min_watt = options.get_minWatt4Grafic()
        
        self.parameters.max_x = int(workout.duration / 60)
        self.parameters.max_y = int(workout.max_power * ftp)
        self.parameters.min_watt = min_watt
        self.parameters.max_cadence = workout.get_max_cadence()
        self.parameters.canvas.delete('all')
        self.workout = workout
        self.parameters.ftp = ftp
        self.draw_first_cadence = True
        self.zeichne_koordinatensystem(workout.get_max_cadence())
        self.hide_tooltip(None)
        self.last_x = self.parameters.x0
        for segment in workout.segments:
            if segment.get_segment_type() == SegmentType.INTERVALST:
                for i in range(segment.get_repeat()):
                    on_power = int(segment.get_power().get_start_power_for_ftp(ftp))
                    off_power = int(segment.get_power().get_end_power_for_ftp(ftp))
                    tags = [_("Dauer") + f" {segment.get_on_duration_as_text()}",]
                    tags.append(_("Leistung") + f" {on_power}")
                    if segment.get_cadence() > 0:
                        tags.append(_("Trittfrequenz") + f" {segment.get_cadence()}")
                    self.zeichne_segment(on_power, 
                                         on_power, 
                                         segment.on_duration / 60,tags,
                                         segment.get_cadence(), 
                                         workout.get_max_cadence())
                    tags = [_("Dauer") + f" {segment.get_off_duration_as_text()}",]
                    tags.append(_("Leistung") + f"{off_power}")
                    if segment.get_cadence() > 0:
                        tags.append(_("Trittfrequenz") + f" {segment.get_cadence()}")
                    self.zeichne_segment(off_power, 
                                         off_power, 
                                         segment.off_duration / 60,tags,
                                         segment.get_cadence(), 
                                         workout.get_max_cadence())
            else:
                start_power = int(segment.get_power().get_start_power_for_ftp(ftp))
                end_power = int(segment.get_power().get_end_power_for_ftp(ftp))

                tags = [_("Dauer") + f" {segment.get_duration_as_text()}",]
                if segment.get_power().start_power == segment.get_power().end_power:
                    tags.append(_("Leistung") + f" {start_power}")
                else:
                    tags.append(_("Leistung") + f" {start_power}/{end_power}")
                dummy = segment.get_cadence()
                if segment.get_cadence() > 0:
                    tags.append(_("Trittfrequenz") + f" {segment.get_cadence()}")
                
                self.zeichne_segment(start_power,
                                     end_power,  
                                     segment.get_duration() / 60,
                                     tags,
                                     segment.get_cadence(), 
                                     workout.get_max_cadence())
