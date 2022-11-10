import os
from collections import namedtuple


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas, erase text instead of drawing if negative=True is specified."""
    
    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break
                
            if symbol == ' ':
                continue

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


def get_frame_size(text):
    """Calculate size of multiline text fragment, return pair — number of rows and columns."""
    
    lines = text.splitlines()
    Size = namedtuple('Size', 'rows columns')
    return Size(rows=len(lines), columns=max([len(line) for line in lines]))


def get_frames(dirpath):
    frames = []
    for filename in os.listdir(dirpath):
        with open(os.path.join(dirpath, filename), 'r') as frame_file:
            frame = frame_file.read()
        frames.append(frame)
    return frames