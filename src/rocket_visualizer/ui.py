"""
User interface and debug information module
"""

import pyglet
from .log_data import LogData


class DebugUI:
    """Handles debug information display"""
    
    def __init__(self, window_width: int, window_height: int):
        self.window_width = window_width
        self.window_height = window_height
    
    def draw_info(self, data: LogData):
        """Draw debug information on screen"""
        info_text = f"Altitude: {data.altitude:.1f}m\n"
        info_text += f"Pitch: {data.pitch:.1f}°\n"
        info_text += f"Accel: {data.acceleration_z:.2f} m/s²"
        
        label = pyglet.text.Label(info_text,
                                font_name='Arial',
                                font_size=12,
                                x=10, y=self.window_height-10,
                                anchor_x='left', anchor_y='top',
                                multiline=True,
                                width=200)
        label.draw()
