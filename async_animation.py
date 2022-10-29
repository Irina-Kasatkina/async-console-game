import asyncio
import curses


async def blink(canvas, row, column, delay=0, symbol='*'):
    """Display animation of blink symbols, delay and symbol can be specified."""

    views = [
        {'state': curses.A_DIM, 'number': 20},
        {'state': curses.A_NORMAL, 'number': 3},
        {'state': curses.A_BOLD, 'number': 5},
        {'state': curses.A_NORMAL, 'number': 3},
    ]

    canvas.addstr(row, column, symbol, views[0]['state'])
    await asyncio.sleep(0)

    for _ in range(delay):
        await asyncio.sleep(0)

    while True:
        for view in views:
            canvas.addstr(row, column, symbol, view['state'])
            for _ in range(view['number']):
                await asyncio.sleep(0)
