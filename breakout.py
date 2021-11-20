"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from campy.graphics.gobjects import GLabel
from breakoutgraphics import BreakoutGraphics, RED, BLACK

# Constant
FRAME_RATE = 100 / 120  # 120 frames per second.
NUM_LIVES = 3


def main():
    graphics = BreakoutGraphics()
    total_bricks = graphics.brick_num
    lives = NUM_LIVES
    score = graphics.score

    # keep playing until no lives left
    while lives > 0:
        while graphics.running:  # will be true after clicked
            vel_x = graphics.get_dx()
            vel_y = graphics.get_dy()
            graphics.ball.move(vel_x, vel_y)
            pause(FRAME_RATE)

            # check coolision
            obj = graphics.check_collision()

            # stop the game if hit all bricks
            if total_bricks == 0:
                break

            # if hits no object, continue
            # otherwise, check which object does the ball hit
            if (
                obj is None
                or obj is graphics.heart1
                or obj is graphics.heart2
                or obj is graphics.heart3
                or obj is graphics.background
            ):
                pass
            else:
                if obj.y < graphics.paddle.y and obj is not graphics.score_label:
                    graphics.window.remove(obj)
                    total_bricks -= 1
                    score += 1
                    graphics.score_label.text = "Score: " + str(score)  # update score
                if obj.y <= graphics.paddle.y:
                    vel_y = -vel_y
                    graphics.set_dy(vel_y)

            # if the ball hits the boundaries, rebound the ball
            if (
                graphics.ball.x <= 0
                or graphics.ball.x >= graphics.window.width - 2 * graphics.ball_radius
            ):
                vel_x = -vel_x
                graphics.set_dx(vel_x)

            if graphics.ball.y <= 0:
                vel_y = -vel_y
                graphics.set_dy(vel_y)

            if graphics.ball.y > graphics.window.height:
                # remove heart pictures
                if lives == 3:
                    graphics.window.remove(graphics.heart3)
                elif lives == 2:
                    graphics.window.remove(graphics.heart2)
                else:
                    graphics.window.remove(graphics.heart1)
                lives -= 1
                graphics.running = False  # the ball wont move til becomes True

                # reset ball position
                if lives > 0:
                    graphics.window.add(
                        graphics.ball,
                        x=(graphics.window.width / 2 - graphics.ball_radius),
                        y=(graphics.window.height / 2 - graphics.ball_radius),
                    )
        pause(FRAME_RATE)
        # stop the game if hit all bricks
        if total_bricks == 0:
            break

    # when win
    if total_bricks == 0:
        graphics.window.remove(graphics.ball)
        pause(FRAME_RATE * 50)
        label_win = GLabel("Great Job!")
        label_win.color = RED
        label_win.font = "Comic Sans MS-50-bold"
        graphics.window.add(
            label_win,
            (graphics.window.width - label_win.width) / 2,
            (graphics.window.height + label_win.height) / 2,
        )

    # when lose
    elif lives == 0:
        graphics.window.remove(graphics.ball)
        pause(FRAME_RATE * 50)
        label_lost = GLabel("Such a Loser")
        label_lost.color = BLACK
        label_lost.font = "Comic Sans MS-50-bold"
        graphics.window.add(
            label_lost,
            (graphics.window.width - label_lost.width) / 2,
            (graphics.window.height + label_lost.height) / 2,
        )


if __name__ == "__main__":
    main()
