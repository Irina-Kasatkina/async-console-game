import asyncio
import curses
from collections import namedtuple
from itertools import product


async def animate(canvas, allowed_area, flame):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = flame.start_row, flame.start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += flame.rows_speed
    column += flame.columns_speed

    symbol = '-' if flame.columns_speed else '|'

    curses.beep()

    while (
        allowed_area.min_row < row < allowed_area.max_row and
        allowed_area.min_column < column < allowed_area.max_column
    ):
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += flame.rows_speed
        column += flame.columns_speed


def create_flames(allowed_area):
    start_row = (allowed_area.max_row - allowed_area.min_row) // 2
    start_column = (allowed_area.max_column - allowed_area.min_column) // 2

    rows_speed = 0.3
    columns_speed = rows_speed * allowed_area.max_column / allowed_area.max_row
    rows_speeds, columns_speeds = [-rows_speed, 0, rows_speed], [-columns_speed, 0, columns_speed]
    speeds = list(product(rows_speeds, columns_speeds))
    speeds.remove((0, 0))

    Flame = namedtuple('Flame', 'start_row start_column rows_speed columns_speed')
    return [
        Flame(start_row=start_row, start_column=start_column, rows_speed=rows_speed, columns_speed=columns_speed)
        for rows_speed, columns_speed in speeds
    ]
