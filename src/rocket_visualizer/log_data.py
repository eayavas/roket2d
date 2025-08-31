"""
Log data handling module for rocket telemetry
"""

import os
import time
import math
import random
from typing import Optional


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
        """Generate a realistic test log line"""
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


class LogReader:
    """Handles reading and parsing log files"""
    
    def __init__(self, log_file_path: Optional[str] = None):
        self.log_file_path = log_file_path
        self.test_generator = TestLogGenerator() if not log_file_path else None
        self.current_data = LogData()
    
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
    
    def read_latest_data(self) -> LogData:
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
        
        return self.current_data
