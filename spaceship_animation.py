import asyncio
import curses
from itertools import cycle

from curses_tools import draw_frame, read_controls


async def animate_spaceship(canvas, row, column, frames):
    canvas_last_row, canvas_last_column = [size - 1 for size in canvas.getmaxyx()]

    spaceship_rows = spaceship_columns = 0
    for frame in frames:
        rows, columns = get_frame_size(frame)
        spaceship_rows = max(spaceship_rows, rows)
        spaceship_columns = max(spaceship_columns, columns)

    previous_row, previous_column, previous_frame = row, column, ''
    for frame in cycle(frames):
        draw_frame(canvas, previous_row, previous_column, previous_frame, negative=True)
        draw_frame(canvas, row, column, frame)
        canvas.border()
        previous_row, previous_column, previous_frame = row, column, frame

        for _ in range(2):
            await asyncio.sleep(0)
            rows_direction, columns_direction, _ = read_controls(canvas)

            if rows_direction:
                row += rows_direction
                if row < 1:
                    row = 1
                elif row > canvas_last_row - spaceship_rows:
                    row = canvas_last_row - spaceship_rows

            if columns_direction:
                column += columns_direction
                if column < 1:
                    column = 1
                elif column > canvas_last_column - spaceship_columns:
                    column = canvas_last_column - spaceship_columns

            if row != previous_row or column != previous_column:
                draw_frame(canvas, previous_row, previous_column, previous_frame, negative=True)
                draw_frame(canvas, row, column, frame)
                previous_row, previous_column, previous_frame = row, column, frame


def get_frame_size(text):
    """Calculate size of multiline text fragment, return pair — number of rows and columns."""
    
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns
