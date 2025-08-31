# Development Guide

## Project Architecture

The Rocket Visualizer follows a modular architecture with clear separation of concerns:

### Core Modules

- **`app.py`** - Main application window and coordination
- **`log_data.py`** - Data parsing and test generation
- **`particles.py`** - Particle effects system
- **`rocket.py`** - Rocket rendering and background effects
- **`ui.py`** - Debug information display

### Data Flow

1. **Log Reading** (`LogReader`) - Reads telemetry every 200ms
2. **Data Processing** - Parses 18-parameter log format
3. **Visualization Update** - Updates rocket orientation, particles, background
4. **Rendering** - 60 FPS display with OpenGL blending

## Development Setup

```bash
# Clone and setup
git clone <repository>
cd roket2d
pip install -r requirements.txt

# Run in development mode
python main.py

# Install as package for testing
pip install -e .
```

## Adding New Features

### New Particle Effects
1. Extend `ParticleSystem` class in `particles.py`
2. Add particle creation method
3. Update `app.py` to call new particle system

### New Telemetry Parameters
1. Update `LogData` class in `log_data.py`
2. Modify `parse_log_line()` method
3. Update visualization logic in relevant modules

### New Visual Elements
1. Create new renderer class in `rocket.py`
2. Add to main rendering loop in `app.py`
3. Update asset loading if needed

## Performance Considerations

- Particle systems use object pooling for efficiency
- Background color updates are cached
- Asset loading happens once at startup
- 60 FPS target with 200ms data updates

## Testing

```bash
# Test with simulated data
python main.py

# Test with real log file
python main.py --log test_data.log

# Test package installation
pip install -e .
rocket-visualizer
```
