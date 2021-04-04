#!/bin/python3
# filters.filesystem v0.1
import os


def fsize_in_range(fpath, min_bytes=0, max_bytes=None) -> bool:
    size = os.path.getsize(fpath)
    max_bytes = size if not max_bytes else max_bytes
    return True if min_bytes <= size <= max_bytes else False

