import curses
import random
import time
from collections import namedtuple
from itertools import product

from async_animation import blink
from fire_animation import fire
from spaceship_animation import animate_spaceship


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
    spaceships_row, spaceships_column, spaceships_frames = get_spaceships(height, width)

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
            animate_spaceship(canvas, spaceships_row, spaceships_column, spaceships_frames)
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
    first_row, last_row = 1, height - 2
    first_column, last_column = 1, width - 2
    min_delay, max_delay = 0, 20
    symbols = '+*.:'

    Star = namedtuple('Star', 'row column symbol delay')
    return [
        Star(
            row=random.randint(first_row, last_row),
            column=random.randint(first_column, last_column),
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


def get_spaceships(height, width):
    filenames = ['frames/rocket_frame_1.txt', 'frames/rocket_frame_2.txt']
    frames = []
    max_rows_count = max_columns_count = 0

    for filename in filenames:
        with open(filename, 'r') as frame_file:
            frame = frame_file.read()

        rows_count, columns_count = count_rows_and_columns(frame)
        max_rows_count = max(max_rows_count, rows_count)
        max_columns_count = max(max_columns_count, columns_count)
        frames.append(frame)

    row = (height - max_rows_count) // 2
    column = (width - max_columns_count) // 2

    return row, column, frames


def count_rows_and_columns(text):
    columns_count = 0
    lines = text.split('\n')
    for line in lines:
        columns_count = max(columns_count, len(line))
    return len(lines), columns_count


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
