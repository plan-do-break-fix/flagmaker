
from PIL import Image

def channel_mean(fpath: str, channel: str):
    _lookup = {"r":0, "g":1, "b":2, "a":3}
    if channel.lower() not in _lookup.keys():
        raise RuntimeError
    with Image.open(fpath) as image:
        index = _lookup[channel.lower()]
        return sum([i[index] for i in image.getdata()])/len(image.getdata())

