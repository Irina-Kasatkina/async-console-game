# coding=utf-8

"""Animate garbage falling."""

import asyncio
import random
import uuid
from collections import namedtuple

import curses_tools
import global_variables
from obstacles import Obstacle


async def fill_orbit_with_garbage(canvas, allowed_area, garbage_frames):
    while True:
        garbage_delay_tics = get_garbage_delay_tics()
        if garbage_delay_tics:
            frame = random.choice(garbage_frames)
            column = random.randint(allowed_area.min_column, allowed_area.max_column)
            frame_size = curses_tools.get_frame_size(frame)
            uid = uuid.uuid4()
            global_variables.coroutines += [fly_garbage(canvas, allowed_area.max_row, column, frame, frame_size, uid)]

        await curses_tools.sleep(garbage_delay_tics or 1)


async def fly_garbage(canvas, max_row, column, frame, frame_size, uid):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""

    speed = 0.5
    row = 0
    while row < max_row:
        global_variables.obstacles.append(Obstacle(row, column, frame_size.rows, frame_size.columns, uid))
        curses_tools.draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)

        for index, obstacle in enumerate(global_variables.obstacles.copy()):
            if obstacle.uid == uid:
                global_variables.obstacles.pop(index)
                break

        curses_tools.draw_frame(canvas, row, column, frame, negative=True)
        if uid in global_variables.obstacles_in_last_collisions:
            global_variables.obstacles_in_last_collisions.remove(uid)
            return
        row += speed


def get_garbage_delay_tics():
    if global_variables.year < 1961:
        return None
    elif global_variables.year < 1969:
        return 20
    elif global_variables.year < 1981:
        return 14
    elif global_variables.year < 1995:
        return 10
    elif global_variables.year < 2010:
        return 8
    elif global_variables.year < 2020:
        return 6
    else:
        return 2
