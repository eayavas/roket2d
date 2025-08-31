"""
Main application window and game loop
"""

import pyglet
from .log_data import LogReader, LogData
from .particles import ParticleSystem
from .rocket import RocketRenderer, BackgroundRenderer
from .ui import DebugUI


class RocketVisualizerApp(pyglet.window.Window):
    """Main application window"""
    
    def __init__(self, log_file_path: str = None, width: int = 600, height: int = 600):
        super().__init__(width, height, caption="Rocket Visualizer")
        
        # Initialize components
        self.log_reader = LogReader(log_file_path)
        self.particle_system = ParticleSystem(width, height)
        self.rocket_renderer = RocketRenderer(width, height)
        self.background_renderer = BackgroundRenderer()
        self.debug_ui = DebugUI(width, height)
        
        # Current data
        self.current_data = LogData()
        
        # Schedule updates
        pyglet.clock.schedule_interval(self.update, 1/60.0)  # 60 FPS
        pyglet.clock.schedule_interval(self.read_log_data, 0.2)  # 200ms log updates
    
    def read_log_data(self, dt):
        """Read the latest log data"""
        self.current_data = self.log_reader.read_latest_data()
    
    def update(self, dt):
        """Update game state"""
        # Update background color based on altitude
        self.background_renderer.update_color(self.current_data.altitude)
        
        # Update rocket rotation based on pitch
        self.rocket_renderer.update_rotation(self.current_data.pitch)
        
        # Create new particles
        self.particle_system.create_exhaust_particles(
            self.width // 2, self.height // 2,
            self.current_data.acceleration_x,
            self.current_data.acceleration_y,
            self.current_data.acceleration_z,
            self.current_data.pitch
        )
        
        self.particle_system.create_dust_particles(
            self.current_data.acceleration_x,
            self.current_data.acceleration_y,
            self.current_data.acceleration_z,
            self.current_data.pitch
        )
        
        # Update particle system
        self.particle_system.update(dt)
    
    def on_draw(self):
        """Render the scene"""
        self.clear()
        
        # Set background color
        self.background_renderer.apply()
        
        # Enable blending for particles
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        
        # Draw components in order
        self.rocket_renderer.draw()
        self.particle_system.draw()
        self.debug_ui.draw_info(self.current_data)
