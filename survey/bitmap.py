
from PIL import Image

def channel_mean(fpath: str, channel: str) -> float:
    _lookup = {"r":0, "g":1, "b":2, "a":3}
    if channel.lower() not in _lookup.keys():
        raise RuntimeError
    with Image.open(fpath) as image:
        with image.convert("RGBA") as rgba:
            index = _lookup[channel.lower()]
            return (sum([i[index] for i in rgba.getdata()])
                    /len(rgba.getdata())

