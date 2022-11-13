# coding=utf-8

"""Manage game."""

import asyncio
import curses
import os
import time
from collections import namedtuple

import fire_animation
import garbage_animation
import global_variables
import obstacles
import stars_animation
import spaceship_animation


BORDER_WIDTH = 1
GARBAGE_FRAMES_DIR = 'frames/garbage'
SPACESHIP_FRAMES_DIR = 'frames/spaceship'
TIC_TIMEOUT = 0.1


def draw(canvas):
    """Draw game field."""
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)

    AllowedArea = namedtuple('AllowedArea', 'min_row min_column max_row max_column')
    max_row, max_column = [last_coordinate - BORDER_WIDTH for last_coordinate in canvas.getmaxyx()]
    allowed_area = AllowedArea(min_row=BORDER_WIDTH, min_column=BORDER_WIDTH, max_row=max_row, max_column=max_column)

    stars = stars_animation.create_stars(allowed_area)
    flames = fire_animation.create_flames(allowed_area)
    spaceship_frames = get_frames(SPACESHIP_FRAMES_DIR)
    garbage_frames = get_frames(GARBAGE_FRAMES_DIR)

    global_variables.coroutines = (
        [stars_animation.blink(canvas, star) for star in stars] +
        [fire_animation.fire(canvas, allowed_area, flame) for flame in flames] +
        [spaceship_animation.fly(canvas, allowed_area, spaceship_frames)] +
        [garbage_animation.fill_orbit_with_garbage(canvas, allowed_area, garbage_frames)] +
        [obstacles.show_obstacles(canvas, global_variables.obstacles)]
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


def get_frames(dirpath):
    """Read frames from files in specified directory."""
    frames = []
    for filename in os.listdir(dirpath):
        with open(os.path.join(dirpath, filename), 'r') as frame_file:
            frame = frame_file.read()
        frames.append(frame)
    return frames


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
