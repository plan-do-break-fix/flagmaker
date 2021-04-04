#!/bin/python3
# filters.bitmap v0.1

import survey.bitmap

def no_transparency() -> bool:
    return True if survey.bitmap.channel_mean("a")==255.0 else False

def conforms_to_palette() -> bool:
    if len(palette) not <= len()

def ncolors_in_range(min_colors=1, max_colors=None) -> bool:
    pass




