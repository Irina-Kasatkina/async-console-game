import curses
import os
import random
import time
from collections import namedtuple
from itertools import product

from async_animation import blink
from fire_animation import fire
from space_garbage import fly_garbage
from spaceship_animation import animate_spaceship


BORDER_WIDTH = 1
GARBAGE_FRAMES_DIR = 'frames/garbage'
SPACESHIP_FRAMES_DIR = 'frames/spaceship'
STARS_COUNT = 200
TIC_TIMEOUT = 0.1


def draw(canvas):
    """Display a gunshot and a spaceship in the sky with blink stars."""

    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)

    height, width = canvas.getmaxyx()
    stars = create_stars(height, width)
    flames = create_flames(height, width)
    spaceship_frames = get_frames(SPACESHIP_FRAMES_DIR)
    garbage_frames = get_frames(GARBAGE_FRAMES_DIR)

    coroutines = (
        [
            blink(canvas, star.row, star.column, delay=star.delay, symbol=star.symbol)
            for star in stars
        ] +
        [
            fire(
                canvas,
                flame.start_row,
                flame.start_column,
                rows_speed=flame.rows_speed,
                columns_speed=flame.columns_speed
            )
            for flame in flames
        ] +
        [
            animate_spaceship(canvas, spaceship_frames)
        ] +
        [
            fly_garbage(canvas, column=10, garbage_frame=random.choice(garbage_frames))
        ]
    )

    while coroutines:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.border()
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)         


def create_stars(height, width):
    min_row, max_row = BORDER_WIDTH, height - BORDER_WIDTH
    min_column, max_column = BORDER_WIDTH, width - BORDER_WIDTH
    min_delay, max_delay = 0, 20
    symbols = '+*.:'

    Star = namedtuple('Star', 'row column symbol delay')
    return [
        Star(
            row=random.randint(min_row, max_row),
            column=random.randint(min_column, max_column),
            symbol=random.choice(symbols),
            delay=random.randint(min_delay, max_delay)
        )
        for _ in range(STARS_COUNT)
    ]


def create_flames(height, width):
    start_row, start_column = height // 2, width // 2

    rows_speed = 0.3
    columns_speed = rows_speed * width / height
    rows_speeds, columns_speeds = [-rows_speed, 0, rows_speed], [-columns_speed, 0, columns_speed]
    speeds = list(product(rows_speeds, columns_speeds))
    speeds.remove((0, 0))

    Flame = namedtuple('Flame', 'start_row start_column rows_speed columns_speed')
    return [
        Flame(
            start_row=start_row,
            start_column=start_column,
            rows_speed=speed[0],
            columns_speed=speed[1]
        )
        for speed in speeds
    ]


def get_frames(dirpath):
    frames = []
    for filename in os.listdir(dirpath):
        with open(os.path.join(dirpath, filename), 'r') as frame_file:
            frame = frame_file.read()
        frames.append(frame)
    return frames


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
