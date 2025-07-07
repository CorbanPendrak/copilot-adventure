# pong.py
# Entry point for the CLI ASCII Pong game

import curses

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
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    required_y = FIELD_HEIGHT + 4  # field + borders + message
    required_x = FIELD_WIDTH + 2   # field + borders
    if max_y < required_y or max_x < required_x:
        stdscr.addstr(0, 0, f"Terminal too small! Resize to at least {required_x}x{required_y}.")
        stdscr.refresh()
        stdscr.getch()
        return
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

def main():
    def demo(stdscr):

        # Default demo positions
        demo_paddle1_y = FIELD_HEIGHT // 2 - PADDLE_HEIGHT // 2
        demo_paddle2_y = FIELD_HEIGHT // 2 - PADDLE_HEIGHT // 2
        demo_ball_x = FIELD_WIDTH // 2
        demo_ball_y = FIELD_HEIGHT // 2
        
        render_game(stdscr, demo_paddle1_y, demo_paddle2_y, demo_ball_x, demo_ball_y)
        stdscr.addstr(FIELD_HEIGHT + 3, 0, "Press any key to exit demo...")
        stdscr.getch()
    
    curses.wrapper(demo)

if __name__ == "__main__":
    main()
