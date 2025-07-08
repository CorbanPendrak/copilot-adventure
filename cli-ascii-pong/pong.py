"""
pong.py.

Entry point for the CLI ASCII Pong game.

Implements a simple ASCII Pong game using the curses library. The game field, paddles, and ball are rendered in the terminal.

The main game loop updates and redraws the game state at a fixed interval, using time.sleep to control the frame rate and reduce CPU usage.

Controls:
    - Press 'q' to quit the game.
    - W/S for left paddle, Up/Down for right paddle (if human players).
"""

import curses
import time
import random
from player import Player
from human_player import HumanPlayer
from follow_ai_player import FollowAIPlayer
from predict_ai_player import PredictAIPlayer
from teleport_ai_player import TeleportAIPlayer

BALL_CHAR = 'O'
FIELD_HEIGHT = 20
FIELD_WIDTH = 40

class GameState:
    """Holds the state of the game for easy passing to AI and rendering."""

    def __init__(self):
        """Initialize the game state."""
        self.left_player = None 
        self.right_player = None
        self.field_height = FIELD_HEIGHT
        self.field_width = FIELD_WIDTH
        self.ball_x = self.field_width // 2
        self.ball_y = self.field_height // 2
        self.ball_dx = 1
        self.ball_dy = 1
        self.score_left = 0
        self.score_right = 0
        self.ball_tick = 0
        self.ball_tick_max = 2
        

def render_game(stdscr, state):
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
            if x == 2 and state.left_player.paddle_y <= y < state.left_player.paddle_y + state.left_player.height:
                line += state.left_player.characters[y - state.left_player.paddle_y]
            elif x == FIELD_WIDTH - 1 and state.right_player.paddle_y <= y < state.right_player.paddle_y + state.right_player.height:
                line += state.right_player.characters[y - state.right_player.paddle_y]
            elif x == state.ball_x and y == state.ball_y:
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
    state = GameState()

    # Initialize players
    state.left_player = TeleportAIPlayer(side='left')
    state.right_player = PredictAIPlayer(side='right')

    while True:
        max_y, max_x = stdscr.getmaxyx()
        if max_y < FIELD_HEIGHT + 4 or max_x < FIELD_WIDTH + 2:
            stdscr.clear()
            stdscr.addstr(0, 0, f"Terminal too small! Resize to at least {FIELD_WIDTH + 2}x{FIELD_HEIGHT + 4}.")
            stdscr.refresh()
            time.sleep(1)
            continue
        render_game(stdscr, state)
        # Display scores (centered)
        score_text = f"{state.score_left} : {state.score_right}"
        score_x = (FIELD_WIDTH + 2 - len(score_text)) // 2
        stdscr.addstr(0, score_x, score_text)
        stdscr.addstr(FIELD_HEIGHT + 3, 0, "Press 'q' to quit. W/S: left paddle, Up/Down: right paddle")
        stdscr.nodelay(True)
        key = stdscr.getch()
        if key == ord('q'):
            break

        # Left paddle (AI or player)
        state.left_player.move(state, key)
        # Right paddle (Up/Down)
        state.right_player.move(state, key)

        # Ball movement (slower)
        state.ball_tick += 1
        if state.ball_tick >= state.ball_tick_max:
            state.ball_x += state.ball_dx
            state.ball_y += state.ball_dy
            state.ball_tick = 0
            # Bounce off top and bottom walls
            if state.ball_y <= 1 or state.ball_y >= FIELD_HEIGHT:
                state.ball_dy *= -1
            # Bounce off left paddle
            if state.ball_x == 3 and state.left_player.paddle_y <= state.ball_y < state.left_player.paddle_y + state.left_player.height:
                state.ball_dx *= -1
            # Bounce off right paddle
            if state.ball_x == FIELD_WIDTH - 2 and state.right_player.paddle_y <= state.ball_y < state.right_player.paddle_y + state.right_player.height:
                state.ball_dx *= -1
            # Score for right player
            if state.ball_x <= 1:
                state.score_right += 1
                state.ball_x = FIELD_WIDTH // 2
                state.ball_y = FIELD_HEIGHT // 2
                state.ball_dx = 1
                state.ball_dy = 1 if state.ball_dy > 0 else -1
                time.sleep(0.5)
                continue
            # Score for left player
            if state.ball_x >= FIELD_WIDTH:
                state.score_left += 1
                state.ball_x = FIELD_WIDTH // 2
                state.ball_y = FIELD_HEIGHT // 2
                state.ball_dx = -1
                state.ball_dy = 1 if state.ball_dy > 0 else -1
                time.sleep(0.5)
                continue
        time.sleep(0.05)  # Controls frame rate and reduces CPU usage

def main():
    """Run the CLI ASCII Pong game using curses."""
    curses.wrapper(game_loop)

if __name__ == "__main__":
    main()
