# pong.py
# Entry point for the CLI ASCII Pong game
#
# This file implements a simple ASCII Pong game using the curses library.
# The game field, paddles, and ball are rendered in the terminal.
#
# The main game loop updates and redraws the game state at a fixed interval (0.1 seconds),
# using time.sleep(0.05) to control the frame rate and reduce CPU usage.
#
# The render_game function checks if the terminal is large enough and waits if not,
# allowing the user to resize the terminal before continuing.
#
# Controls:
#   - Press 'q' to quit the game.

import curses
import time

FIELD_HEIGHT = 20
FIELD_WIDTH = 40
PADDLE_HEIGHT = 4
PADDLE_CHAR = '|'
BALL_CHAR = 'O'

# Example positions for demonstration
paddle1_y = 8
paddle2_y = 8
ball_x = 20
ball_y = 10

def render_game(stdscr, paddle1_y, paddle2_y, ball_x, ball_y):
    """
    Render the game field, paddles, and ball using ASCII characters.

    If the terminal is too small, display a warning and keep checking every second
    until the terminal is resized to a sufficient size.
    """
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        required_y = FIELD_HEIGHT + 4  # field + borders + message
        required_x = FIELD_WIDTH + 2   # field + borders
        if max_y < required_y or max_x < required_x:
            stdscr.addstr(0, 0, f"Terminal too small! Resize to at least {required_x}x{required_y}.")
            stdscr.refresh()
            time.sleep(1)
            continue
        break
    # Draw top border
    stdscr.addstr(0, 0, '+' + '-' * FIELD_WIDTH + '+')
    # Draw field, paddles, and ball
    for y in range(1, FIELD_HEIGHT + 1):
        line = '|'
        for x in range(1, FIELD_WIDTH + 1):
            if x == 2 and paddle1_y <= y < paddle1_y + PADDLE_HEIGHT:
                line += PADDLE_CHAR
            elif x == FIELD_WIDTH - 1 and paddle2_y <= y < paddle2_y + PADDLE_HEIGHT:
                line += PADDLE_CHAR
            elif x == ball_x and y == ball_y:
                line += BALL_CHAR
            else:
                line += ' '
        line += '|'
        stdscr.addstr(y, 0, line)
    # Draw bottom border
    stdscr.addstr(FIELD_HEIGHT + 1, 0, '+' + '-' * FIELD_WIDTH + '+')
    stdscr.refresh()

def game_loop(stdscr):
    """
    Update and render the game state at a fixed interval (0.1 seconds).

    Use time.sleep(0.1) to control the frame rate and reduce CPU usage.
    Handle paddle movement: 'w'/'s' for left, up/down for right.
    Implement ball movement, bouncing logic, and scoring.
    Also check if the terminal is resized too small during gameplay.
    """
    # Initial positions
    paddle1_y = FIELD_HEIGHT // 2 - PADDLE_HEIGHT // 2
    paddle2_y = FIELD_HEIGHT // 2 - PADDLE_HEIGHT // 2
    ball_x = FIELD_WIDTH // 2
    ball_y = FIELD_HEIGHT // 2
    ball_dx = 1  # Ball movement direction (x)
    ball_dy = 1  # Ball movement direction (y)
    score_left = 0
    score_right = 0
    ball_tick = 0
    ball_tick_max = 2  # Ball moves every 2 frames (slower)
    required_y = FIELD_HEIGHT + 4
    required_x = FIELD_WIDTH + 2

    while True:
        max_y, max_x = stdscr.getmaxyx()
        if max_y < required_y or max_x < required_x:
            stdscr.clear()
            stdscr.addstr(0, 0, f"Terminal too small! Resize to at least {required_x}x{required_y}.")
            stdscr.refresh()
            time.sleep(1)
            continue
        render_game(stdscr, paddle1_y, paddle2_y, ball_x, ball_y)
        # Display scores
        stdscr.addstr(0, FIELD_WIDTH // 2 - 5, f"{score_left} : {score_right}")
        stdscr.addstr(FIELD_HEIGHT + 3, 0, "Press 'q' to quit. W/S: left paddle, Up/Down: right paddle")
        stdscr.nodelay(True)
        key = stdscr.getch()
        if key == ord('q'):
            break
        # Left paddle (W/S)
        if key == ord('w') and paddle1_y > 1:
            paddle1_y -= 1
        elif key == ord('s') and paddle1_y < FIELD_HEIGHT - PADDLE_HEIGHT + 1:
            paddle1_y += 1
        # Right paddle (Up/Down)
        elif key == curses.KEY_UP and paddle2_y > 1:
            paddle2_y -= 1
        elif key == curses.KEY_DOWN and paddle2_y < FIELD_HEIGHT - PADDLE_HEIGHT + 1:
            paddle2_y += 1

        # Ball movement (slower)
        ball_tick += 1
        if ball_tick >= ball_tick_max:
            ball_x += ball_dx
            ball_y += ball_dy
            ball_tick = 0

            # Bounce off top and bottom walls
            if ball_y <= 1 or ball_y >= FIELD_HEIGHT:
                ball_dy *= -1
            # Bounce off left paddle
            if ball_x == 3 and paddle1_y <= ball_y < paddle1_y + PADDLE_HEIGHT:
                ball_dx *= -1
            # Bounce off right paddle
            if ball_x == FIELD_WIDTH - 2 and paddle2_y <= ball_y < paddle2_y + PADDLE_HEIGHT:
                ball_dx *= -1
            # Score for right player
            if ball_x <= 1:
                score_right += 1
                ball_x = FIELD_WIDTH // 2
                ball_y = FIELD_HEIGHT // 2
                ball_dx = 1
                ball_dy = 1 if ball_dy > 0 else -1
                time.sleep(0.5)
                continue
            # Score for left player
            if ball_x >= FIELD_WIDTH:
                score_left += 1
                ball_x = FIELD_WIDTH // 2
                ball_y = FIELD_HEIGHT // 2
                ball_dx = -1
                ball_dy = 1 if ball_dy > 0 else -1
                time.sleep(0.5)
                continue

        time.sleep(0.05)  # Controls frame rate and reduces CPU usage

def main():
    """Run the CLI ASCII Pong game using curses."""
    curses.wrapper(game_loop)

if __name__ == "__main__":
    main()
