"""
player.py.

Defines the abstract base Player class for the ASCII Pong game.
"""

from abc import ABC, abstractmethod


class Player(ABC):
    """Abstract base class for a Pong player (human or AI).

    Subclasses must implement the move method.
    """

    def __init__(self, side="left"):
        """Initialize a player with a side ('left' or 'right')."""
        self.side = side
        self.height = 4
        self.paddle_y = 20 // 2 - self.height // 2
        self.characters = ["|"] * self.height

    @abstractmethod
    def move(self, state, key=None):
        """Move the paddle based on user input or AI logic. key is the keypress for this frame."""
        pass
