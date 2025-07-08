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
import sys

try:
    import winsound  # For Windows
except ImportError:
    winsound = None

from player import Player
from human_player import HumanPlayer
from follow_ai_player import FollowAIPlayer
from predict_ai_player import PredictAIPlayer
from teleport_ai_player import TeleportAIPlayer

BALL_CHAR = 'O'
FIELD_HEIGHT = 20
FIELD_WIDTH = 40
BEEPING = False  # Set to True to enable beeping sounds
PLAYER_TYPES = {
    'Human': HumanPlayer,
    'Follow AI': FollowAIPlayer,
    'Predict AI': PredictAIPlayer,
    'Teleport AI': TeleportAIPlayer
}

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

def start_screen(stdscr):
    """
    Display the start screen with instructions and wait for user input to start the game.
    
    The screen will show the game title, instructions, and wait for any key press to begin.
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

    # Draw field
    for y in range(1, FIELD_HEIGHT + 1):
        stdscr.addstr(y, 0, '|' + " " * FIELD_WIDTH + '|')

    message = "Welcome to CLI ASCII Pong!"
    stdscr.addstr(FIELD_HEIGHT // 2, FIELD_WIDTH // 2 - len(message) // 2, message)
    message = "Press space to start."
    stdscr.addstr(FIELD_HEIGHT // 2 + 1, FIELD_WIDTH // 2 - len(message) // 2, message)

    # Draw bottom border
    stdscr.addstr(FIELD_HEIGHT + 1, 0, '+' + '-' * FIELD_WIDTH + '+')

    # Print players
    player_keys = list(PLAYER_TYPES.keys())
    for (i, player_type) in enumerate(player_keys):
        stdscr.addstr(FIELD_HEIGHT // 2 + i + 3, 4, f"{player_type}")
        stdscr.addstr(FIELD_HEIGHT // 2 + i + 3, FIELD_WIDTH - len(player_type) - 4, f"{player_type}")
    

    stdscr.addstr(FIELD_HEIGHT // 2 + 3, 2, '->')
    stdscr.addstr(FIELD_HEIGHT // 2 + 3, FIELD_WIDTH - 4, '<-')

    # Player selection
    left_selection = 0
    right_selection = 0
    while True:
        key = stdscr.getch()  # Wait for any key press
        if key is None:
            continue
        elif key == ord(' ') or key == curses.KEY_ENTER:
            break
        elif key == ord('w') and left_selection > 0:
            left_selection -= 1
        elif key == ord('s') and left_selection < len(PLAYER_TYPES) - 1:
            left_selection += 1
        elif key == curses.KEY_UP and right_selection > 0:
            right_selection -= 1
        elif key == curses.KEY_DOWN and right_selection < len(PLAYER_TYPES) - 1:
            right_selection += 1
        
        # Highlight selected players
        for i in range(len(PLAYER_TYPES)):
            stdscr.addstr(FIELD_HEIGHT // 2 + i + 3, 2, '  ')
            stdscr.addstr(FIELD_HEIGHT // 2 + i + 3, FIELD_WIDTH - 4, '  ')
            if i == left_selection:
                stdscr.addstr(FIELD_HEIGHT // 2 + i + 3, 2, '->')
            if i == right_selection:
                stdscr.addstr(FIELD_HEIGHT // 2 + i + 3, FIELD_WIDTH - 4, '<-')
        
        time.sleep(0.1)

    return (PLAYER_TYPES[player_keys[left_selection]],
            PLAYER_TYPES[player_keys[right_selection]])

def end_screen(stdscr, state):
    """Display the end screen with the final score and wait for a key press to exit."""
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

    # Draw field
    for y in range(1, FIELD_HEIGHT + 1):
        stdscr.addstr(y, 0, '|' + " " * FIELD_WIDTH + '|')

    message = "Final Score"
    stdscr.addstr(FIELD_HEIGHT // 2, FIELD_WIDTH // 2 - len(message) // 2, message)
    message = f"{state.score_left} : {state.score_right}"
    stdscr.addstr(FIELD_HEIGHT // 2 + 1, FIELD_WIDTH // 2 - len(message) // 2, message)
    message = "Press any key to exit."
    stdscr.addstr(FIELD_HEIGHT // 2 + 3, FIELD_WIDTH // 2 - len(message) // 2, message)

    # Draw bottom border
    stdscr.addstr(FIELD_HEIGHT + 1, 0, '+' + '-' * FIELD_WIDTH + '+')
    stdscr.refresh()

    stdscr.nodelay(False)
    stdscr.getch()  # Wait for any key press
    stdscr.clear()


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


def beep(event='default'):
    """Play a beep sound (cross-platform, different tones for events)."""
    if BEEPING == False:
        return
    if sys.platform.startswith('win') and winsound:
        if event == 'score':
            winsound.Beep(1500, 150)
        elif event == 'paddle':
            winsound.Beep(900, 80)
        else:
            winsound.Beep(1000, 100)
    else:
        # On Unix, use ASCII bell, but print different number for different events
        if event == 'score':
            print('\a', end='', flush=True)
            time.sleep(0.05)
            print('\a', end='', flush=True)
        elif event == 'paddle':
            print('\a', end='', flush=True)
        else:
            print('\a', end='', flush=True)

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
    players = start_screen(stdscr)
    state.left_player = players[0](side='left')
    state.right_player = players[1](side='right')

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
                beep('paddle')  # Paddle bounce
            # Bounce off right paddle
            if state.ball_x == FIELD_WIDTH - 2 and state.right_player.paddle_y <= state.ball_y < state.right_player.paddle_y + state.right_player.height:
                state.ball_dx *= -1
                beep('paddle')  # Paddle bounce
            # Score for right player
            if state.ball_x <= 1:
                state.score_right += 1
                state.ball_x = FIELD_WIDTH // 2
                state.ball_y = FIELD_HEIGHT // 2
                state.ball_dx = 1
                state.ball_dy = 1 if state.ball_dy > 0 else -1
                beep('score')  # Score
                time.sleep(0.5)
                continue
            # Score for left player
            if state.ball_x >= FIELD_WIDTH:
                state.score_left += 1
                state.ball_x = FIELD_WIDTH // 2
                state.ball_y = FIELD_HEIGHT // 2
                state.ball_dx = -1
                state.ball_dy = 1 if state.ball_dy > 0 else -1
                beep('score')  # Score
                time.sleep(0.5)
                continue
        time.sleep(0.05)  # Controls frame rate and reduces CPU usage

    end_screen(stdscr, state)

def main():
    """Run the CLI ASCII Pong game using curses."""
    curses.wrapper(game_loop)

if __name__ == "__main__":
    main()
