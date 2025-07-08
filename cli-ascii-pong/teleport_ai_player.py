"""
teleport_ai_player.py.

Implements the TeleportAIPlayer class for the ASCII Pong game.
"""

from player import Player

class TeleportAIPlayer(Player):
    """Represents an AI player that teleports to the ball's y position."""

    def __init__(self, side='left'):
        """Initialize a teleport AI player with a given side."""
        super().__init__(side)
        self.height = 1
        self.characters = [(">" if side == "left" else "<")] * self.height
        
    def move(self, state, key=None):
        """Teleport the paddle to the ball's y position if within range."""
        if (self.side == 'right' and state.ball_x >= state.field_width - 4) or (self.side == 'left' and state.ball_x <= 4):
            offset = 1 if state.ball_dy > 0 else -1
            self.paddle_y = max(1, min(state.ball_y + offset, state.field_height - self.height + 1))
