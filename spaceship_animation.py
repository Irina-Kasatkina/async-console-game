import asyncio
from itertools import cycle

from curses_tools import draw_frame, read_controls


BORDER_WIDTH = 1


async def animate_spaceship(canvas, frames):
    max_row, max_column = canvas.getmaxyx()
    max_row, max_column = max_row - BORDER_WIDTH, max_column - BORDER_WIDTH
    frame_height, frame_width = get_frame_size(frames[0])
    row, column = (max_row - frame_height) // 2, (max_column - frame_width) // 2

    for frame in cycle(frames):
        for _ in range(2):
            rows_direction, columns_direction, _ = read_controls(canvas)
            row = normalize_coordinate(row + rows_direction, max_row - frame_height)
            column = normalize_coordinate(column + columns_direction, max_column - frame_width)
            draw_frame(canvas, row, column, frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, frame, negative=True)


def get_frame_size(text):
    """Calculate size of multiline text fragment, return pair — number of rows and columns."""
    
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


def normalize_coordinate(coordinate, max_coordinate):
    return min(max_coordinate, max(BORDER_WIDTH, coordinate))
