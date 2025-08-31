# Rocket Visualizer

A real-time rocket visualization application that displays a rocket with orientation, particle effects, and environmental changes based on log data.

## Features

- **Real-time rocket orientation** based on pitch angle from log data
- **Dynamic background color** that changes from light blue to dark blue based on altitude (0-5000m)
- **Particle effects** for rocket exhaust based on acceleration data
- **Speed-based dust particles** for motion sensation
- **Meter/compass background** for reference
- **Test mode** when no log file is provided

## Project Structure

```
roket2d/
├── main.py                    # Main entry point
├── src/
│   └── rocket_visualizer/
│       ├── __init__.py        # Package initialization
│       ├── app.py             # Main application window
│       ├── log_data.py        # Log file handling and parsing
│       ├── particles.py       # Particle system effects
│       ├── rocket.py          # Rocket rendering and background
│       └── ui.py              # Debug UI components
├── assets/
│   ├── roket.png             # Rocket sprite
│   └── meter.png             # Background meter
├── requirements.txt          # Dependencies
└── README.md                # This file
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Development Mode

#### With log file:
```bash
python main.py --log path/to/logfile.txt
```

#### Test mode (generates simulated data):
```bash
python main.py
```

#### With particle effects enabled:
```bash
python main.py --particles
python main.py --log path/to/logfile.txt --particles
```

### Installation Mode

#### Install the package:
```bash
pip install -e .
```

#### Run after installation:
```bash
rocket-visualizer --log path/to/logfile.txt
# or
rocket-visualizer
# With particles enabled
rocket-visualizer --particles
rocket-visualizer --log path/to/logfile.txt --particles
```

## Log Format

The application expects log data in the following format (18 space-separated values per line):
```
timestamp altitude pressure temperature gps_altitude latitude longitude gyro_x gyro_y gyro_z acceleration_x acceleration_y acceleration_z pitch yaw roll battery state
```

Example:
```
14:31:05.797 853.553 919.43 24.26 0 0 0 0 0 0 -0.0654297 -0.0424805 1.09863 -3.40572 0 0 3.58732e-43 1
```

## Controls

- The application updates automatically every 200ms
- Press ESC or close the window to exit

## Assets

Make sure the following assets are in the `assets/` folder:
- `roket.png` - Rocket image
- `meter.png` - Background meter/compass image
