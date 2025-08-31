#!/usr/bin/env python3
"""
Rocket Visualizer - Main Entry Point
A real-time rocket visualization application using Pyglet
"""

import argparse
import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pyglet
from rocket_visualizer.app import RocketVisualizerApp


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description='Rocket Visualization Application')
    parser.add_argument('--log', type=str, help='Path to log file')
    parser.add_argument('--particles', action='store_true', help='Enable particle effects')
    args = parser.parse_args()
    
    # Create and run the application
    app = RocketVisualizerApp(args.log, enable_particles=args.particles)
    pyglet.app.run()


if __name__ == '__main__':
    main()
