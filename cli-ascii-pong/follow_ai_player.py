"""
follow_ai_player.py.

Implements the FollowAIPlayer class for the ASCII Pong game.
"""

import random
from player import Player


class FollowAIPlayer(Player):
    """Represents an AI player that follows the ball's y position."""

    def __init__(self, side="left"):
        """Initialize a follow AI player with a given side."""
        super().__init__(side)
        self.characters = ["(" if side == "right" else ")"] * self.height

    def move(self, state, key=None):
        """Move the paddle to follow the ball's y position with some randomness."""
        paddle_center = self.paddle_y + self.height // 2
        if random.random() < 0.8:
            if state.ball_y < paddle_center and self.paddle_y > 1:
                self.paddle_y -= 1
            elif (
                state.ball_y > paddle_center
                and self.paddle_y < state.field_height - self.height + 1
            ):
                self.paddle_y += 1
