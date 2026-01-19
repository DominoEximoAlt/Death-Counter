# Death Counter for Souls-like Games

A simple tool to track the number of player deaths in challenging, Souls-like games. Useful for streamers, speedrunners, or anyone wanting to monitor their progress and improvement over time.

## Features

- **Automatic Death Detection:** Uses screen capture and image processing to detect death screens in supported games.
- **Game Selector:** Easily choose which game to track from a list of supported titles.
- **Overlay Support:** Display death count and timer as an overlay on your screen.
- **Persistent Data:** Death counts and session time are saved between runs.

## Tech Stack

- **Python 3.11+**
- **mss:** For fast cross-platform screen capturing.
- **NumPy:** For efficient image array processing.
- **OpenCV (optional):** For advanced image processing (commented out in code).
- **dotenv:** For environment variable management.
- **ctypes:** For Windows-specific screen size detection.
- **JSON:** For persistent storage of death counts and session time.

## Getting Started


## Supported Games

- Lords of the Fallen 2  
