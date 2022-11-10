import asyncio
from itertools import cycle
from collections import namedtuple

import controls
import fire_animation
import frames_functions
import global_variables
import physics


SPACESHIP_FRAMES_DIR = 'frames/spaceship'
SPACESHIP_AND_SHOT_SPEED_DELTA = 0.3


async def animate(canvas, spaceship):
    frame_size = frames_functions.get_frame_size(spaceship.frames[0])
    row = (spaceship.allowed_area.max_row - frame_size.rows) // 2
    column = (spaceship.allowed_area.max_column - frame_size.columns) // 2
    row_speed = column_speed = 0
    from_left_to_nose = (len(spaceship.frames[0][0]) - len(spaceship.frames[0][0].lstrip())) + 1

    for frame in cycle(spaceship.frames):
        for _ in range(2):
            rows_direction, columns_direction, space_pressed = controls.read_controls(canvas)
            row_speed, column_speed = physics.update_speed(row_speed, column_speed, rows_direction, columns_direction)
            row, column = (
                normalize_coordinates(row + row_speed, column + column_speed, spaceship, frame_size)
            )
            if space_pressed:
                nose_column = column + from_left_to_nose
                flame_row_speed = row_speed - SPACESHIP_AND_SHOT_SPEED_DELTA
                flame = fire_animation.create_flame(row, nose_column, flame_row_speed, column_speed=0)
                global_variables.coroutines += [fire_animation.animate(canvas, spaceship.allowed_area, flame)]

            frames_functions.draw_frame(canvas, row, column, frame)
            await asyncio.sleep(0)
            frames_functions.draw_frame(canvas, row, column, frame, negative=True)


def create_spaceship(allowed_area):
    spaceship_frames = frames_functions.get_frames(SPACESHIP_FRAMES_DIR)
    Spaceship = namedtuple('Spaceship', 'allowed_area frames')
    return Spaceship(allowed_area=allowed_area, frames=spaceship_frames)


def normalize_coordinates(row, column, spaceship, frame_size):
    return (
        min(spaceship.allowed_area.max_row - frame_size.rows, max(spaceship.allowed_area.min_row, row)),
        min(spaceship.allowed_area.max_column - frame_size.columns, max(spaceship.allowed_area.min_column, column))
    )
