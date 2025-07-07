# CLI ASCII Pong Game

A command-line Pong game rendered in ASCII art.

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
- [ ] Create the main game loop to update and render the game state at a fixed interval
- [ ] Handle user input for paddle movement (e.g., W/S or Up/Down keys)

### 4. Game Mechanics
- [ ] Implement ball movement and bouncing logic
- [ ] Add collision detection for paddles and walls
- [ ] Track and display scores for both players

### 5. Single & Multiplayer
- [ ] Implement single-player mode (player vs. simple AI)
- [ ] Add two-player mode (both paddles controlled by users)

### 6. Polish & Features
- [ ] Add a start screen and game over screen
- [ ] Display instructions and controls
- [ ] Add difficulty settings (ball speed, paddle size)
- [ ] Optional: Add sound effects (beep on bounce/score)

### 7. Packaging & Distribution
- [ ] Add a command-line entry point for easy execution
- [ ] Write usage instructions in the README
- [ ] Package for distribution (e.g., PyPI, npm)
