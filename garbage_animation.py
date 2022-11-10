import asyncio
import random
from collections import namedtuple

import common
import frames


GARBAGE_FRAMES_DIR = 'frames/garbage'


def create_garbage(allowed_area):
    garbage_frames = frames.get_frames(GARBAGE_FRAMES_DIR)
    Garbage = namedtuple('Garbage', 'allowed_area frames')
    return Garbage(allowed_area=allowed_area, frames=garbage_frames)


async def fill_orbit_with_garbage(canvas, garbage):
    while True:
        garbage_frame = random.choice(garbage.frames)
        column = random.randint(garbage.allowed_area.min_column, garbage.allowed_area.max_column)

        common.coroutines += [fly_garbage(canvas, garbage.allowed_area.max_row, column, garbage_frame)]
        for _ in range(random.randint(8, 18)):
            await asyncio.sleep(0)


async def fly_garbage(canvas, max_row, column, frame):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""

    speed = 0.5
    row = 0
    while row < max_row:
        frames.draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        frames.draw_frame(canvas, row, column, frame, negative=True)
        row += speed