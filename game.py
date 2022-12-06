# coding=utf-8

"""Manage game."""

import asyncio
import curses
import os
import time
from collections import namedtuple

import curses_tools
import fire_animation
import garbage_animation
import global_variables
import obstacles
import stars_animation
import spaceship_animation


BORDER_WIDTH = 1
GAME_SECONDS_IN_YEAR = 1.5
GAMEOVER_FRAME_DIR = 'frames/gameover'
GARBAGE_FRAMES_DIR = 'frames/garbage'
INFO_WINDOW_ROWS = 1
PHRASES = {
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}
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
    info_window_columns = len(str(global_variables.year)) + max([len(phrase) for phrase in PHRASES.values()]) + 1
    info_window = canvas.derwin(INFO_WINDOW_ROWS, info_window_columns, max_row-INFO_WINDOW_ROWS, BORDER_WIDTH)

    stars = stars_animation.create_stars(allowed_area)
    flames = fire_animation.create_flames(allowed_area)
    spaceship_frames = get_frames(SPACESHIP_FRAMES_DIR)
    garbage_frames = get_frames(GARBAGE_FRAMES_DIR)

    global_variables.coroutines = (
        [stars_animation.blink(canvas, star) for star in stars] +
        [fire_animation.fire(canvas, allowed_area, flame) for flame in flames] +
        [spaceship_animation.run_spaceship(canvas, allowed_area, spaceship_frames)] +
        [garbage_animation.fill_orbit_with_garbage(canvas, allowed_area, garbage_frames)] +
        [show_message(info_window)] +
        [change_year()]
    )

    while global_variables.coroutines:
        exhausted_coroutines = []
        for coroutine in global_variables.coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                exhausted_coroutines.append(coroutine)

        canvas.border()
        info_window.refresh()
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)

        try:
            for exhausted_coroutine in exhausted_coroutines:
                global_variables.coroutines.remove(exhausted_coroutine)
        except ValueError:                
            global_variables.coroutines = [show_gameover(canvas)]


def get_frames(dirpath):
    """Read frames from files in specified directory."""

    frames = []
    for filename in os.listdir(dirpath):
        with open(os.path.join(dirpath, filename), 'r') as frame_file:
            frame = frame_file.read()
        frames.append(frame)
    return frames


async def show_message(info_window):
    """Display year and event in info_window."""

    while True:
        message = f"{global_variables.year} {PHRASES.get(global_variables.year, '')}"
        curses_tools.draw_frame(info_window, 0, 0, message)
        await asyncio.sleep(0)
        curses_tools.draw_frame(info_window, 0, 0, message, negative=True)


async def change_year():
    """Change year if GAME_SECONDS_IN_YEAR seconds have passed."""

    year_start = time.time()
    while True:
        await asyncio.sleep(0)
        if time.time() - year_start >= GAME_SECONDS_IN_YEAR:
            global_variables.year += 1
            year_start += GAME_SECONDS_IN_YEAR


async def show_gameover(canvas):
    """Display gameover message."""

    frame = get_frames(GAMEOVER_FRAME_DIR)[0]
    curses_tools.draw_frame(canvas, start_row=8, start_column=10, text=frame)
    await curses_tools.sleep(20)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
