#!/usr/bin/env python3
"""
Setup script for Rocket Visualizer
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rocket-visualizer",
    version="1.0.0",
    author="Rocket Visualizer Team",
    description="A real-time rocket visualization application using Pyglet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/roket2d",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Games/Entertainment :: Simulation",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "rocket-visualizer=rocket_visualizer.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/*.png"],
    },
)
