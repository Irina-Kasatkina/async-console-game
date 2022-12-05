# coding=utf-8

"""Animate fire, flames, shots."""

import asyncio
import curses
from collections import namedtuple
from itertools import product

import global_variables


async def fire(canvas, allowed_area, flame):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = flame.start_row, flame.start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += flame.row_speed
    column += flame.column_speed

    symbol = '-' if flame.column_speed else '|'

    curses.beep()

    while (
        allowed_area.min_row < row < allowed_area.max_row and
        allowed_area.min_column < column < allowed_area.max_column
    ):
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += flame.row_speed
        column += flame.column_speed
        for obstacle in global_variables.obstacles:
            if obstacle.has_collision(row, column):
                global_variables.obstacles_in_last_collisions.append(obstacle.uid)
                return


def create_flames(allowed_area):
    start_row = (allowed_area.max_row - allowed_area.min_row) // 2
    start_column = (allowed_area.max_column - allowed_area.min_column) // 2

    row_speed = 0.3
    column_speed = row_speed * allowed_area.max_column / allowed_area.max_row
    rows_speeds, columns_speeds = [-row_speed, 0, row_speed], [-column_speed, 0, column_speed]
    speeds = list(product(rows_speeds, columns_speeds))
    speeds.remove((0, 0))

    return [
        create_flame(start_row, start_column, row_speed, column_speed)
        for row_speed, column_speed in speeds
    ]


def create_flame(start_row, start_column, row_speed, column_speed):
    Flame = namedtuple('Flame', 'start_row start_column row_speed column_speed')
    return Flame(start_row=start_row, start_column=start_column, row_speed=row_speed, column_speed=column_speed)
