#!/bin/python3
# filters.bitmap v0.1

bitmaps = ["bmp", "gif", "jpg", "png"]

import survey.bitmap

def no_transparency(fpath) -> bool:
    return True if survey.bitmap.channel_mean(fpath, "a") == 255.0 else False

def conforms_to_palette() -> bool:
    #if len(palette) > len()
    pass

def ncolors_in_range(min_colors=1, max_colors=None) -> bool:
    pass




