# coding=utf-8

"""Contain common project functions."""

import asyncio
from collections import namedtuple


def get_frame_size(text):
    """Calculate size of multiline text fragment, return pair — number of rows and columns."""
    
    lines = text.splitlines()
    Size = namedtuple('Size', 'rows columns')
    return Size(rows=len(lines), columns=max([len(line) for line in lines]))


async def sleep(tics=1):
    for _ in range(tics):
        await asyncio.sleep(0)
