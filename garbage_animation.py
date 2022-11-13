# coding=utf-8

"""Animate garbage falling."""

import asyncio
import random
import uuid
from collections import namedtuple

import common_functions
import curses_tools
import global_variables
from obstacles import Obstacle


async def fill_orbit_with_garbage(canvas, allowed_area, garbage_frames):
    while True:
        frame = random.choice(garbage_frames)
        column = random.randint(allowed_area.min_column, allowed_area.max_column)

        frame_size = common_functions.get_frame_size(frame)
        uid = uuid.uuid4()
        global_variables.coroutines += [fly_garbage(canvas, allowed_area.max_row, column, frame, frame_size, uid)]
        await common_functions.sleep(random.randint(8, 18))


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
        row += speed
