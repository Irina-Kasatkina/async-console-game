import curses
import time
from collections import namedtuple

import fire_animation
import garbage_animation
import global_variables
import stars_animation
import spaceship_animation


BORDER_WIDTH = 1
TIC_TIMEOUT = 0.1


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)

    AllowedArea = namedtuple('AllowedArea', 'min_row min_column max_row max_column')
    max_row, max_column = [last_coordinate - BORDER_WIDTH for last_coordinate in canvas.getmaxyx()]
    allowed_area = AllowedArea(min_row=BORDER_WIDTH, min_column=BORDER_WIDTH, max_row=max_row, max_column=max_column)

    stars = stars_animation.create_stars(allowed_area)
    flames = fire_animation.create_flames(allowed_area)
    spaceship = spaceship_animation.create_spaceship(allowed_area)
    garbage = garbage_animation.create_garbage(allowed_area)

    global_variables.coroutines = (
        [stars_animation.animate(canvas, star) for star in stars] +
        [fire_animation.animate(canvas, allowed_area, flame) for flame in flames] +
        [spaceship_animation.animate(canvas, spaceship)] +
        [garbage_animation.fill_orbit_with_garbage(canvas, garbage)]
    )

    while global_variables.coroutines:
        for coroutine in global_variables.coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                global_variables.coroutines.remove(coroutine)

        canvas.border()
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
