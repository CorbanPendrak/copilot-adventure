# CLI ASCII Pong Game

![GitHub Copilot](https://img.shields.io/badge/github_copilot-8957E5?style=flat&logo=github-copilot&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
[![macOS](https://img.shields.io/badge/mac%20os-000000?style=flat&logo=macos&logoColor=F0F0F0)](https://github.com/CorbanPendrak/copilot-adventure/releases/latest)
[![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white)](https://github.com/CorbanPendrak/copilot-adventure/releases/latest)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)](https://github.com/CorbanPendrak/copilot-adventure/releases/latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

A command-line Pong game rendered in ASCII art.

## About This Project
- This project uses [pydocstyle](https://www.pydocstyle.org/) to enforce Python docstring conventions and maintain high-quality documentation.
- **Benefits of pydocstyle:**
    - Ensures every public module, class, method, and function has a docstring.
    - Checks for proper formatting and style of docstrings (PEP 257 compliance).
    - Helps keep code understandable and maintainable for all contributors.
    - Automatically runs on every commit to catch documentation issues early.

## Usage Instructions

### Running with Python

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   - On Windows, also run:
     ```bash
     pip install windows-curses
     ```
2. **Run the game:**
   ```bash
   python pong.py
   ```
   Or, if you made it executable:
   ```bash
   ./pong.py
   ```

### Running as a Standalone Executable

You can package the game as a single-file executable (no Python required) using [PyInstaller](https://pyinstaller.org/):

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```
2. **Build the executable:**
   ```bash
   pyinstaller --onefile pong.py
   ```
3. **Find the executable in the `dist/` folder:**
   - On Linux/macOS: `dist/pong`
   - On Windows: `dist/pong.exe`
4. **Run the executable:**
   ```bash
   ./dist/pong    # or pong.exe on Windows
   ```

### Controls
- Left paddle: W/S keys
- Right paddle: Up/Down arrow keys
- Press `q` to quit

### Notes
- The game requires a terminal window of at least 42x24 characters.
- Sound effects are optional and can be enabled in the code (`BEEPING = True`).
- On Windows, you must install the `windows-curses` package for keyboard support.

## Roadmap: Building a CLI ASCII Pong Game

### 1. Project Setup
- [x] Choose a programming language (e.g., Python, Node.js)
- [x] Set up the project structure and initialize version control

### 2. Terminal Rendering
- [x] Research and select a method/library for terminal screen clearing and input handling (`curses`)
    - `curses` is a built-in Python library designed for creating text-based user interfaces in the terminal.
    - It allows for efficient screen clearing and redrawing, reducing flicker and making real-time games smoother.
    - Supports non-blocking keyboard input, which is essential for responsive paddle movement.
    - Cross-platform (works on Linux and macOS by default; on Windows, install `windows-curses` via pip).
    - No external dependencies required for most systems, making setup simple and portable.
- [x] Implement a function to render the game field, paddles, and ball using ASCII characters

### 3. Game Loop
- [x] Create the main game loop to update and render the game state at a fixed interval
- [x] Handle user input for paddle movement (e.g., W/S or Up/Down keys)

### 4. Game Mechanics
- [x] Implement ball movement and bouncing logic
- [x] Add collision detection for paddles and walls
- [x] Track and display scores for both players

### 5. Single & Multiplayer
- [x] Implement single-player mode (player vs. simple AI)
- [x] Implement multiple AI types
- [x] Add two-player mode (both paddles controlled by users)

### 6. Polish & Features
- [x] Add a start screen and game over screen
- [x] Display instructions and controls
- [x] Optional: Add sound effects (beep on bounce/score)

### 7. Packaging
- [x] Add a command-line entry point for easy execution
- [x] Write usage instructions in the README
