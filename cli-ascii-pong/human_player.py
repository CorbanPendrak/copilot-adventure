"""
human_player.py.

Implements the HumanPlayer class for the ASCII Pong game.
"""

import curses
from player import Player

class HumanPlayer(Player):
    """Represents a human player who controls the paddle with keyboard input."""

    def __init__(self, side='left'):
        """Initialize a human player with a given side."""
        super().__init__(side)
        self.characters = ["|"] * self.height
        
    def move(self, state, key=None):
        """Move the paddle based on keyboard input and game state."""
        if key is None:
            return self.paddle_y
        if self.side == 'left':
            if key == ord('w') and self.paddle_y > 1:
                self.paddle_y -= 1
            elif key == ord('s') and self.paddle_y < state.field_height - self.height + 1:
                self.paddle_y += 1
        else:
            if key == curses.KEY_UP and self.paddle_y > 1:
                self.paddle_y -= 1
            elif key == curses.KEY_DOWN and self.paddle_y < state.field_height - self.height + 1:
                self.paddle_y += 1
