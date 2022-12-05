# coding=utf-8

"""Animate movement of spacehip."""

import asyncio
from itertools import cycle

import controls
import curses_tools
import fire_animation
import global_variables
import physics


SPACESHIP_AND_SHOT_SPEED_DELTA = 0.3


async def fly(canvas, allowed_area, spaceship_frames):
    frame_size = curses_tools.get_frame_size(spaceship_frames[0])
    row = (allowed_area.max_row - frame_size.rows) // 2
    column = (allowed_area.max_column - frame_size.columns) // 2
    row_speed = column_speed = 0
    from_left_to_nose = (len(spaceship_frames[0][0]) - len(spaceship_frames[0][0].lstrip())) + 1

    for frame in cycle(spaceship_frames):
        for _ in range(2):
            rows_direction, columns_direction, space_pressed = controls.read_controls(canvas)
            row_speed, column_speed = physics.update_speed(row_speed, column_speed, rows_direction, columns_direction)
            row, column = (
                normalize_coordinates(row + row_speed, column + column_speed, allowed_area, frame_size)
            )
            if space_pressed:
                nose_column = column + from_left_to_nose
                flame_row_speed = row_speed - SPACESHIP_AND_SHOT_SPEED_DELTA
                flame = fire_animation.create_flame(row, nose_column, flame_row_speed, column_speed=0)
                global_variables.coroutines += [fire_animation.fire(canvas, allowed_area, flame)]

            curses_tools.draw_frame(canvas, row, column, frame)
            await asyncio.sleep(0)
            curses_tools.draw_frame(canvas, row, column, frame, negative=True)


def normalize_coordinates(row, column, allowed_area, frame_size):
    return (
        min(allowed_area.max_row - frame_size.rows, max(allowed_area.min_row, row)),
        min(allowed_area.max_column - frame_size.columns, max(allowed_area.min_column, column))
    )
