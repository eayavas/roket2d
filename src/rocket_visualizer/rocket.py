"""
Rocket visualization and rendering module
"""

import pyglet
from typing import Tuple


class RocketRenderer:
    """Handles rocket sprite loading and rendering"""
    
    def __init__(self, window_width: int, window_height: int):
        self.window_width = window_width
        self.window_height = window_height
        self.rocket_sprite = None
        self.meter_sprite = None
        self.load_assets()
    
    def load_assets(self):
        """Load rocket and meter images"""
        try:
            # Load rocket image
            rocket_img = pyglet.image.load('assets/roket.png')
            rocket_img.anchor_x = rocket_img.width // 2
            rocket_img.anchor_y = rocket_img.height // 2
            self.rocket_sprite = pyglet.sprite.Sprite(rocket_img, 
                                                    x=self.window_width//2, 
                                                    y=self.window_height//2)
            
            # Load meter image (background)
            meter_img = pyglet.image.load('assets/meter.png')
            meter_img.anchor_x = meter_img.width // 2
            meter_img.anchor_y = meter_img.height // 2
            self.meter_sprite = pyglet.sprite.Sprite(meter_img,
                                                   x=self.window_width//2,
                                                   y=self.window_height//2)
            # Scale meter to fit behind rocket
            self.meter_sprite.scale = 0.8
            
        except Exception as e:
            print(f"Error loading assets: {e}")
            # Create placeholder sprites if assets fail to load
            self.rocket_sprite = None
            self.meter_sprite = None
    
    def update_rotation(self, pitch: float):
        """Update rocket rotation based on pitch angle"""
        if self.rocket_sprite:
            self.rocket_sprite.rotation = -pitch  # Negative for correct direction
    
    def draw(self):
        """Draw rocket and meter sprites"""
        # Draw meter (background)
        if self.meter_sprite:
            self.meter_sprite.draw()
        
        # Draw rocket
        if self.rocket_sprite:
            self.rocket_sprite.draw()


class BackgroundRenderer:
    """Handles background color rendering based on altitude"""
    
    def __init__(self):
        self.bg_color = (135, 206, 235)  # Default sky blue
    
    def update_color(self, altitude: float):
        """Update background color based on altitude (0-5000m range)"""
        altitude = max(0, min(5000, altitude))
        # Interpolate from light blue (low altitude) to dark blue (high altitude)
        ratio = altitude / 5000.0
        
        # Light blue to dark blue gradient
        light_blue = (135, 206, 235)  # Sky blue
        dark_blue = (25, 25, 112)     # Midnight blue
        
        r = int(light_blue[0] * (1 - ratio) + dark_blue[0] * ratio)
        g = int(light_blue[1] * (1 - ratio) + dark_blue[1] * ratio)
        b = int(light_blue[2] * (1 - ratio) + dark_blue[2] * ratio)
        
        self.bg_color = (r, g, b)
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get current background color"""
        return self.bg_color
    
    def apply(self):
        """Apply background color to OpenGL context"""
        pyglet.gl.glClearColor(
            self.bg_color[0]/255.0, 
            self.bg_color[1]/255.0, 
            self.bg_color[2]/255.0, 
            1.0
        )
