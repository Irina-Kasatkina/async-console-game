import asyncio
from itertools import cycle
from collections import namedtuple

import controls
import frames


SPACESHIP_FRAMES_DIR = 'frames/spaceship'


async def animate(canvas, spaceship):
    frame_size = frames.get_frame_size(spaceship.frames[0])
    row = (spaceship.allowed_area.max_row - frame_size.rows) // 2
    column = (spaceship.allowed_area.max_column - frame_size.columns) // 2

    for frame in cycle(spaceship.frames):
        for _ in range(2):
            rows_speed, columns_speed, _ = controls.read_controls(canvas)
            row, column = (
                normalize_coordinates(row + rows_speed, column + columns_speed, spaceship, frame_size)
            )
            frames.draw_frame(canvas, row, column, frame)
            await asyncio.sleep(0)
            frames.draw_frame(canvas, row, column, frame, negative=True)


def create_spaceship(allowed_area):
    spaceship_frames = frames.get_frames(SPACESHIP_FRAMES_DIR)
    Spaceship = namedtuple('Spaceship', 'allowed_area frames')
    return Spaceship(allowed_area=allowed_area, frames=spaceship_frames)


def normalize_coordinates(row, column, spaceship, frame_size):
    return (
        min(spaceship.allowed_area.max_row - frame_size.rows, max(spaceship.allowed_area.min_row, row)),
        min(spaceship.allowed_area.max_column - frame_size.columns, max(spaceship.allowed_area.min_column, column))
    )
