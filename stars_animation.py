import asyncio
import curses
import random
from collections import namedtuple


STARS_COUNT = 200


async def animate(canvas, star):
    """Display animation of blink symbols, delay and symbol can be specified."""

    views = [
        {'state': curses.A_DIM, 'number': 20},
        {'state': curses.A_NORMAL, 'number': 3},
        {'state': curses.A_BOLD, 'number': 5},
        {'state': curses.A_NORMAL, 'number': 3},
    ]

    canvas.addstr(star.row, star.column, star.symbol, views[0]['state'])
    await asyncio.sleep(0)

    for _ in range(star.delay):
        await asyncio.sleep(0)

    while True:
        for view in views:
            canvas.addstr(star.row, star.column, star.symbol, view['state'])
            for _ in range(view['number']):
                await asyncio.sleep(0)


def create_stars(allowed_area):
    min_delay, max_delay = 0, 20
    symbols = '+*.:'

    Star = namedtuple('Star', 'row column symbol delay')
    return [
        Star(
            row=random.randint(allowed_area.min_row, allowed_area.max_row),
            column=random.randint(allowed_area.min_column, allowed_area.max_column),
            symbol=random.choice(symbols),
            delay=random.randint(min_delay, max_delay)
        )
        for _ in range(STARS_COUNT)
    ]
