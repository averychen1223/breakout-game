"""
Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.graphics.gimage import GImage
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random


BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40  # Height of a brick (in pixels).
BRICK_HEIGHT = 20  # Height of a brick (in pixels).
BRICK_ROWS = 10  # Number of rows of bricks.
BRICK_COLS = 10  # Number of columns of bricks.
BRICK_OFFSET = (
    50  # Vertical offset of the topmost brick from the window top (in pixels).
)
BALL_RADIUS = 10  # Radius of the ball (in pixels).
PADDLE_WIDTH = 75  # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels).
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 10  # Initial vertical speed for the ball.
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball.
FRAME_RATE = 10

# Color settings
RED = (237, 84, 133)
GREEN = (87, 209, 201)
YELLOW = (255, 251, 203)
BLACK = (0, 0, 0)


class BreakoutGraphics:
    def __init__(
        self,
        ball_radius=BALL_RADIUS,
        paddle_width=PADDLE_WIDTH,
        paddle_height=PADDLE_HEIGHT,
        paddle_offset=PADDLE_OFFSET,
        brick_rows=BRICK_ROWS,
        brick_cols=BRICK_COLS,
        brick_width=BRICK_WIDTH,
        brick_height=BRICK_HEIGHT,
        brick_offset=BRICK_OFFSET,
        brick_spacing=BRICK_SPACING,
        title="Breakout",
    ):
        self.paddle_width = paddle_width
        self.paddle_height = paddle_height
        self.paddle_offset = paddle_offset
        self.brick_rows = brick_rows
        self.brick_cols = brick_cols
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.brick_spacing = brick_spacing
        self.ball_radius = ball_radius
        self.brick_offset = brick_offset
        self.brick_num = self.brick_rows * self.brick_cols

        # Create a graphical window, with some extra space.
        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (
            brick_rows * (brick_height + brick_spacing) - brick_spacing
        )
        self.window = GWindow(
            width=self.window_width, height=self.window_height, title=title
        )

        # background
        self.background = GImage("img/opening_background.jpeg")
        self.window.add(self.background)

        # create score board
        self.create_score_board()

        # create a paddle.
        self.create_paddle()

        # center a filled ball in the graphical window.
        self.create_ball()

        # Initialize our mouse listeners.
        self.running = False

        # add heart
        self.heart1 = GImage("img/heart.png")
        self.heart2 = GImage("img/heart.png")
        self.heart3 = GImage("img/heart.png")
        self.window.add(self.heart1, 410, 10)
        self.window.add(self.heart2, 380, 10)
        self.window.add(self.heart3, 350, 10)

        # draw bricks
        self.draw_bricks()

        # default initial velocity for the ball.
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -self.__dx
        self.__dy = INITIAL_Y_SPEED

        # game start
        onmouseclicked(self.game_start)
        onmousemoved(self.move_paddle)

    def get_dx(self):
        """
        Getter function for horizontal speed
        """
        return self.__dx

    def get_dy(self):
        """
        Getter function for vertical speed
        """
        return self.__dy

    def set_dx(self, dx):
        """
        Setter function for horizontal speed
        """
        self.__dx = dx

    def set_dy(self, dy):
        """
        Setter function for vertical speed
        """
        self.__dy = dy

    def game_start(self, m):
        """
        Caller function to start the gae
        """
        self.running = True

    def move_paddle(self, m):
        """
        Function to move the paddle with mouse
        """
        if m.x <= self.paddle.width / 2:
            self.paddle.x = 0
        elif m.x >= self.window.width - self.paddle.width / 2:
            self.paddle.x = self.window.width - self.paddle.width
        else:
            self.paddle.x = m.x - self.paddle.width / 2

    def create_score_board(self):
        """
        Create the score board
        """
        self.score = 0
        self.score_label = GLabel("Score: " + str(self.score))
        self.score_label.font = "Comic Sans MS-20-bold"
        self.window.add(self.score_label, 0, 10 + self.score_label.height)

    def create_ball(self):
        """
        Create the ball
        """
        self.ball = GOval(
            2 * self.ball_radius,
            2 * self.ball_radius,
            x=(self.window_width / 2 - self.ball_radius),
            y=(self.window_height / 2 - self.ball_radius),
        )
        self.ball.filled = True
        self.ball.color = "black"
        self.window.add(self.ball)

    def create_paddle(self):
        """
        Create the paddle
        """
        self.paddle = GRect(
            self.paddle_width,
            self.paddle_height,
            x=(self.window_width / 2 - self.paddle_width / 2),
            y=(self.window_height - self.paddle_offset),
        )
        self.paddle.filled = True
        self.paddle.color = "black"
        self.window.add(self.paddle)

    def draw_bricks(self):
        """
        Draw bricks on the screen
        """
        for i in range(self.brick_cols):
            for j in range(self.brick_rows):
                brick = GRect(
                    self.brick_width,
                    self.brick_height,
                    x=j * (self.brick_width + self.brick_spacing),
                    y=self.brick_offset + i * (self.brick_height + self.brick_spacing),
                )
                brick.filled = True
                if i < 3:
                    brick.fill_color = RED
                    brick.color = RED
                elif i >= 3 and i < 6:
                    brick.fill_color = GREEN
                    brick.color = GREEN
                else:
                    brick.fill_color = YELLOW
                    brick.color = YELLOW
                self.window.add(brick)

    def check_collision(self):
        """
        Check if the ball collides with other objects
        Return None if no collision, else, return the object
        """
        upper_left_x = int(self.ball.x)
        upper_left_y = int(self.ball.y)
        for new_x in range(
            upper_left_x, upper_left_x + 3 * self.ball_radius, 2 * self.ball_radius
        ):
            for new_y in range(
                upper_left_y, upper_left_y + 3 * self.ball_radius, 2 * self.ball_radius
            ):
                # see if this position has object
                obj = self.window.get_object_at(new_x, new_y)

                # return object if not None
                if obj is not None:
                    return obj

        # no collision
        return None
