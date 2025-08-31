#!/usr/bin/env python3
"""
Rocket Visualization Application
Displays a rocket with real-time orientation based on log data
"""

import pyglet
import math
import random
import argparse
import os
import time
import threading
from typing import Optional, Tuple, List

# Window dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

class Particle:
    """Particle class for exhaust and dust effects"""
    def __init__(self, x: float, y: float, vx: float, vy: float, life: float, color: Tuple[int, int, int, int]):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = random.uniform(1, 3)
    
    def update(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        
        # Fade out over time
        alpha = int(255 * (self.life / self.max_life))
        self.color = (self.color[0], self.color[1], self.color[2], max(0, alpha))
    
    def is_alive(self) -> bool:
        return self.life > 0

class LogData:
    """Data structure for parsed log entries"""
    def __init__(self):
        self.timestamp = ""
        self.altitude = 0.0
        self.pressure = 0.0
        self.temperature = 0.0
        self.gps_altitude = 0.0
        self.latitude = 0.0
        self.longitude = 0.0
        self.gyro_x = 0.0
        self.gyro_y = 0.0
        self.gyro_z = 0.0
        self.acceleration_x = 0.0
        self.acceleration_y = 0.0
        self.acceleration_z = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.roll = 0.0
        self.battery = 0.0
        self.state = 0

class TestLogGenerator:
    """Generates test log data when no log file is provided"""
    def __init__(self):
        self.time_start = time.time()
        self.altitude = 0.0
        self.pitch = 0.0
    
    def generate_line(self) -> str:
        current_time = time.time()
        elapsed = current_time - self.time_start
        
        # Simulate ascending rocket with slight right lean
        self.altitude += 10.0  # 10m per update
        self.pitch = math.sin(elapsed * 0.5) * 15.0  # Oscillating pitch ±15 degrees
        
        # Generate realistic-looking data
        pressure = 1013.25 - (self.altitude * 0.12)  # Decreasing pressure with altitude
        temperature = 15.0 - (self.altitude * 0.0065)  # Temperature lapse rate
        
        # Acceleration data (simulated thrust)
        accel_z = 9.81 + random.uniform(5, 15)  # Upward acceleration
        accel_x = random.uniform(-0.5, 0.5)
        accel_y = random.uniform(-0.5, 0.5)
        
        timestamp = time.strftime("%H:%M:%S.") + f"{int((current_time % 1) * 1000):03d}"
        
        return f"{timestamp} {self.altitude:.3f} {pressure:.2f} {temperature:.2f} 0 0 0 0 0 0 {accel_x:.6f} {accel_y:.6f} {accel_z:.5f} {self.pitch:.5f} 0 0 0 1\n"

class RocketVisualizer(pyglet.window.Window):
    """Main application window"""
    
    def __init__(self, log_file_path: Optional[str] = None):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, caption="Rocket Visualizer")
        
        self.log_file_path = log_file_path
        self.test_generator = TestLogGenerator() if not log_file_path else None
        self.current_data = LogData()
        
        # Load assets
        self.load_assets()
        
        # Particle systems
        self.exhaust_particles: List[Particle] = []
        self.dust_particles: List[Particle] = []
        
        # Background color (will change based on altitude)
        self.bg_color = (135, 206, 235)  # Sky blue
        
        # Schedule updates
        pyglet.clock.schedule_interval(self.update, 1/60.0)  # 60 FPS
        pyglet.clock.schedule_interval(self.read_log_data, 0.2)  # 200ms log updates
        
    def load_assets(self):
        """Load rocket and meter images"""
        try:
            # Load rocket image
            rocket_img = pyglet.image.load('assets/roket.png')
            rocket_img.anchor_x = rocket_img.width // 2
            rocket_img.anchor_y = rocket_img.height // 2
            self.rocket_sprite = pyglet.sprite.Sprite(rocket_img, 
                                                    x=WINDOW_WIDTH//2, 
                                                    y=WINDOW_HEIGHT//2)
            
            # Load meter image (background)
            meter_img = pyglet.image.load('assets/meter.png')
            meter_img.anchor_x = meter_img.width // 2
            meter_img.anchor_y = meter_img.height // 2
            self.meter_sprite = pyglet.sprite.Sprite(meter_img,
                                                   x=WINDOW_WIDTH//2,
                                                   y=WINDOW_HEIGHT//2)
            # Scale meter to fit behind rocket
            self.meter_sprite.scale = 0.8
            
        except Exception as e:
            print(f"Error loading assets: {e}")
            # Create placeholder sprites if assets fail to load
            self.rocket_sprite = None
            self.meter_sprite = None
    
    def parse_log_line(self, line: str) -> Optional[LogData]:
        """Parse a single log line into LogData structure"""
        try:
            parts = line.strip().split()
            if len(parts) < 18:
                return None
            
            data = LogData()
            data.timestamp = parts[0]
            data.altitude = float(parts[1])
            data.pressure = float(parts[2])
            data.temperature = float(parts[3])
            data.gps_altitude = float(parts[4])
            data.latitude = float(parts[5])
            data.longitude = float(parts[6])
            data.gyro_x = float(parts[7])
            data.gyro_y = float(parts[8])
            data.gyro_z = float(parts[9])
            data.acceleration_x = float(parts[10])
            data.acceleration_y = float(parts[11])
            data.acceleration_z = float(parts[12])
            data.pitch = float(parts[13])
            data.yaw = float(parts[14])
            data.roll = float(parts[15])
            data.battery = float(parts[16])
            data.state = int(parts[17])
            
            return data
        except (ValueError, IndexError) as e:
            print(f"Error parsing log line: {e}")
            return None
    
    def read_log_data(self, dt):
        """Read the latest log data"""
        if self.test_generator:
            # Generate test data
            line = self.test_generator.generate_line()
            data = self.parse_log_line(line)
            if data:
                self.current_data = data
        elif self.log_file_path and os.path.exists(self.log_file_path):
            try:
                with open(self.log_file_path, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        data = self.parse_log_line(last_line)
                        if data:
                            self.current_data = data
            except Exception as e:
                print(f"Error reading log file: {e}")
    
    def update_background_color(self):
        """Update background color based on altitude (0-5000m range)"""
        altitude = max(0, min(5000, self.current_data.altitude))
        # Interpolate from light blue (low altitude) to dark blue (high altitude)
        ratio = altitude / 5000.0
        
        # Light blue to dark blue gradient
        light_blue = (135, 206, 235)  # Sky blue
        dark_blue = (25, 25, 112)     # Midnight blue
        
        r = int(light_blue[0] * (1 - ratio) + dark_blue[0] * ratio)
        g = int(light_blue[1] * (1 - ratio) + dark_blue[1] * ratio)
        b = int(light_blue[2] * (1 - ratio) + dark_blue[2] * ratio)
        
        self.bg_color = (r, g, b)
    
    def create_exhaust_particles(self):
        """Create exhaust particles based on acceleration data"""
        # Calculate thrust magnitude from acceleration
        accel_magnitude = math.sqrt(
            self.current_data.acceleration_x**2 + 
            self.current_data.acceleration_y**2 + 
            self.current_data.acceleration_z**2
        )
        
        # Create particles proportional to acceleration
        num_particles = int(accel_magnitude * 2)  # Scale factor
        
        for _ in range(num_particles):
            # Position particles at rocket's exhaust (bottom)
            rocket_x = WINDOW_WIDTH // 2
            rocket_y = WINDOW_HEIGHT // 2
            
            # Offset for exhaust position (behind rocket)
            angle_rad = math.radians(self.current_data.pitch)
            exhaust_offset = 40  # Distance behind rocket center
            
            x = rocket_x - math.sin(angle_rad) * exhaust_offset
            y = rocket_y - math.cos(angle_rad) * exhaust_offset
            
            # Random velocity for particle spread
            vx = random.uniform(-50, 50) - math.sin(angle_rad) * 100
            vy = random.uniform(-50, 50) - math.cos(angle_rad) * 100
            
            # Orange/red exhaust colors
            color = (255, random.randint(100, 200), 0, 255)
            life = random.uniform(0.5, 1.5)
            
            particle = Particle(x, y, vx, vy, life, color)
            self.exhaust_particles.append(particle)
    
    def create_dust_particles(self):
        """Create dust particles for speed sensation"""
        # Calculate speed from acceleration (simplified)
        speed = abs(self.current_data.acceleration_z) * 10  # Scale factor
        
        num_particles = int(speed * 0.5)
        
        for _ in range(num_particles):
            # Random position around screen edges
            if random.choice([True, False]):
                x = random.choice([0, WINDOW_WIDTH])
                y = random.uniform(0, WINDOW_HEIGHT)
            else:
                x = random.uniform(0, WINDOW_WIDTH)
                y = random.choice([0, WINDOW_HEIGHT])
            
            # Velocity towards rocket (creating streaking effect)
            rocket_x = WINDOW_WIDTH // 2
            rocket_y = WINDOW_HEIGHT // 2
            
            dx = rocket_x - x
            dy = rocket_y - y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 0:
                vx = (dx / distance) * speed * 2
                vy = (dy / distance) * speed * 2
            else:
                vx = vy = 0
            
            # White/gray dust colors
            gray = random.randint(150, 255)
            color = (gray, gray, gray, 128)
            life = random.uniform(1.0, 2.0)
            
            particle = Particle(x, y, vx, vy, life, color)
            self.dust_particles.append(particle)
    
    def update(self, dt):
        """Update game state"""
        self.update_background_color()
        
        # Update rocket rotation based on pitch
        if self.rocket_sprite:
            self.rocket_sprite.rotation = -self.current_data.pitch  # Negative for correct direction
        
        # Create new particles
        self.create_exhaust_particles()
        self.create_dust_particles()
        
        # Update existing particles
        self.exhaust_particles = [p for p in self.exhaust_particles if p.is_alive()]
        self.dust_particles = [p for p in self.dust_particles if p.is_alive()]
        
        for particle in self.exhaust_particles + self.dust_particles:
            particle.update(dt)
    
    def draw_particle(self, particle: Particle):
        """Draw a single particle"""
        # Use pyglet's shape module for better compatibility
        circle = pyglet.shapes.Circle(particle.x, particle.y, particle.size, 
                                    color=particle.color[:3], batch=None)
        circle.opacity = particle.color[3]
        circle.draw()
    
    def on_draw(self):
        """Render the scene"""
        self.clear()
        
        # Set background color
        pyglet.gl.glClearColor(self.bg_color[0]/255.0, self.bg_color[1]/255.0, self.bg_color[2]/255.0, 1.0)
        
        # Enable blending for particles
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        
        # Draw meter (background)
        if self.meter_sprite:
            self.meter_sprite.draw()
        
        # Draw dust particles (behind rocket)
        for particle in self.dust_particles:
            self.draw_particle(particle)
        
        # Draw rocket
        if self.rocket_sprite:
            self.rocket_sprite.draw()
        
        # Draw exhaust particles (in front of rocket)
        for particle in self.exhaust_particles:
            self.draw_particle(particle)
        
        # Draw debug info
        self.draw_debug_info()
    
    def draw_debug_info(self):
        """Draw debug information on screen"""
        info_text = f"Altitude: {self.current_data.altitude:.1f}m\n"
        info_text += f"Pitch: {self.current_data.pitch:.1f}°\n"
        info_text += f"Accel: {self.current_data.acceleration_z:.2f} m/s²"
        
        label = pyglet.text.Label(info_text,
                                font_name='Arial',
                                font_size=12,
                                x=10, y=WINDOW_HEIGHT-10,
                                anchor_x='left', anchor_y='top',
                                multiline=True,
                                width=200)
        label.draw()

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description='Rocket Visualization Application')
    parser.add_argument('--log', type=str, help='Path to log file')
    args = parser.parse_args()
    
    # Create and run the application
    app = RocketVisualizer(args.log)
    pyglet.app.run()

if __name__ == '__main__':
    main()
