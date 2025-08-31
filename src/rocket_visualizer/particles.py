"""
Particle system module for rocket visualization effects
"""

import math
import random
from typing import List, Tuple
import pyglet


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
        """Update particle position and fade"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        
        # Fade out over time
        alpha = int(255 * (self.life / self.max_life))
        self.color = (self.color[0], self.color[1], self.color[2], max(0, alpha))
    
    def is_alive(self) -> bool:
        """Check if particle is still alive"""
        return self.life > 0
    
    def draw(self):
        """Draw the particle"""
        circle = pyglet.shapes.Circle(self.x, self.y, self.size, 
                                    color=self.color[:3], batch=None)
        circle.opacity = self.color[3]
        circle.draw()


class ParticleSystem:
    """Manages particle effects for the rocket visualization"""
    
    def __init__(self, window_width: int, window_height: int, enabled: bool = False):
        self.window_width = window_width
        self.window_height = window_height
        self.enabled = enabled
        self.exhaust_particles: List[Particle] = []
        self.dust_particles: List[Particle] = []
    
    def create_exhaust_particles(self, rocket_x: float, rocket_y: float, 
                               acceleration_x: float, acceleration_y: float, 
                               acceleration_z: float, pitch: float):
        """Create exhaust particles based on acceleration data"""
        if not self.enabled:
            return
            
        # Calculate thrust magnitude from acceleration
        accel_magnitude = math.sqrt(acceleration_x**2 + acceleration_y**2 + acceleration_z**2)
        
        # Create particles proportional to acceleration
        num_particles = int(accel_magnitude * 2)  # Scale factor
        
        for _ in range(num_particles):
            # Offset for exhaust position (behind rocket)
            angle_rad = math.radians(pitch)
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
    
    def create_dust_particles(self, acceleration_x: float, acceleration_y: float, 
                            acceleration_z: float, pitch: float):
        """Create dust particles for speed sensation - particles flow from nose to tail direction"""
        if not self.enabled:
            return
            
        # Calculate speed from acceleration magnitude
        speed_magnitude = math.sqrt(acceleration_x**2 + acceleration_y**2 + acceleration_z**2)
        
        # Particle generation rate based on speed (more particles when faster)
        base_rate = 3  # Base particles per frame
        speed_multiplier = max(0.1, speed_magnitude * 0.5)  # Scale factor
        num_particles = int(base_rate * speed_multiplier)
        
        # Get rocket angle in radians
        angle_rad = math.radians(pitch)
        
        for _ in range(num_particles):
            # Calculate the nose direction vector
            nose_dx = math.sin(angle_rad)  # X component of nose direction
            nose_dy = math.cos(angle_rad)  # Y component of nose direction
            
            # Find intersection with canvas edges in nose direction
            center_x = self.window_width // 2
            center_y = self.window_height // 2
            
            # Calculate how far we need to go to reach canvas edge
            if abs(nose_dx) > abs(nose_dy):
                # Will hit left or right edge first
                if nose_dx > 0:
                    t = (self.window_width - center_x) / nose_dx
                else:
                    t = -center_x / nose_dx
            else:
                # Will hit top or bottom edge first
                if nose_dy > 0:
                    t = (self.window_height - center_y) / nose_dy
                else:
                    t = -center_y / nose_dy
            
            # Calculate the edge position
            edge_x = center_x + nose_dx * t
            edge_y = center_y + nose_dy * t
            
            # Add some randomness along the edge
            perpendicular_dx = -nose_dy  # Perpendicular to nose direction
            perpendicular_dy = nose_dx
            
            random_offset = random.uniform(-100, 100)
            start_x = edge_x + perpendicular_dx * random_offset
            start_y = edge_y + perpendicular_dy * random_offset
            
            # Clamp to canvas bounds
            start_x = max(0, min(self.window_width, start_x))
            start_y = max(0, min(self.window_height, start_y))
            
            # Velocity is opposite to nose direction (particles flow from nose to tail)
            particle_speed = speed_magnitude * 50  # Scale factor for visual effect
            vx = -nose_dx * particle_speed
            vy = -nose_dy * particle_speed
            
            # Add some randomness to velocity
            vx += random.uniform(-20, 20)
            vy += random.uniform(-20, 20)
            
            # White/gray dust colors with some variation
            gray = random.randint(180, 255)
            color = (gray, gray, gray, random.randint(100, 200))
            life = random.uniform(2.0, 4.0)  # Longer life for better streaking
            
            particle = Particle(start_x, start_y, vx, vy, life, color)
            self.dust_particles.append(particle)
    
    def update(self, dt: float):
        """Update all particles"""
        # Update existing particles
        self.exhaust_particles = [p for p in self.exhaust_particles if p.is_alive()]
        self.dust_particles = [p for p in self.dust_particles if p.is_alive()]
        
        for particle in self.exhaust_particles + self.dust_particles:
            particle.update(dt)
    
    def draw(self):
        """Draw all particles"""
        # Draw dust particles (behind rocket)
        for particle in self.dust_particles:
            particle.draw()
        
        # Draw exhaust particles (in front of rocket)
        for particle in self.exhaust_particles:
            particle.draw()
