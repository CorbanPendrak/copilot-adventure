"""
predict_ai_player.py.

Implements the PredictAIPlayer class for the ASCII Pong game.
"""

from player import Player


class PredictAIPlayer(Player):
    """Represents an AI player that predicts the ball's y position and moves accordingly."""

    def __init__(self, side="left"):
        """Initialize a predictive AI player with a given side."""
        super().__init__(side)
        self.characters = ["+"] + ["|"] * (self.height - 2) + ["+"]
        self.predicted_pos = 0

    def move(self, state, key=None):
        """Smarter AI: predict ball's y position, accounting for wall bounces, and move only as needed, using the game state."""
        # Predict where the ball will be when it reaches the paddle's x position
        if self.side == "left" and state.ball_dx < 0:
            target_x = 3
        elif self.side == "right" and state.ball_dx > 0:
            target_x = state.field_width - 2
        else:
            # Reset predicted position if not moving toward paddle
            self.predicted_pos = 0
            return  # Ball not moving toward this paddle

        # Simulate ball's y position as it travels to the paddle
        if self.predicted_pos == 0:
            sim_y = state.ball_y
            sim_dy = state.ball_dy
            sim_x = state.ball_x
            count = 0
            # Limit iterations to prevent infinite loop
            while sim_x != target_x and count < 100:
                sim_x += state.ball_dx
                sim_y += sim_dy
                if sim_y <= 1 or sim_y >= state.field_height:
                    sim_dy *= -1
                count += 1

            self.predicted_pos = sim_y

        # Now move paddle toward predicted y
        paddle_center = self.paddle_y + self.height // 2
        if self.predicted_pos < self.paddle_y + 1 and self.paddle_y > 1:
            self.paddle_y -= 1
        elif (
            self.predicted_pos >= self.paddle_y - 1 + self.height
            and self.paddle_y < state.field_height - self.height + 1
        ):
            self.paddle_y += 1
