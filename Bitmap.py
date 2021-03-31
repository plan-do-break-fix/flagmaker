from collections import Counter
from typing import List, Tuple

from PIL import Image


def basename(fname):
    fname = ".".join(fname.split(".")[:-1])
    return fname


def all_pixels(image: Image):
    """Return all image pixels as an array of RGBA tuples."""
    return [image.getpixel((i,j))
            for j in range(0,image.height)
            for i in range(0,image.width)]


def composite_mean(pixels: List[Tuple[int]]) -> List[int]:
    totals = [sum([px[i] for px in pixels]) for i in range(0,4)]
    return [total/len(pixels) for total in totals]


def composite_mode(pixels: List[Tuple[int]]) -> Tuple[List[int]]:
    channels = [[px[i] for px in pixels] for i in range(0,4)]
    return [[k for k, v in Counter(channel).items()
                if v == Counter(channel).most_common(1)[0][1]][0]
            for channel in channels]


def square(image):
    d = max(image.width, image.height)
    image.resize((d, d))
    return image