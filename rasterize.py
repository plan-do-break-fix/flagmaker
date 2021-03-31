import os
from PIL import Image
from wand.image import Image

import Vector as vg

def rasterize(path_in, path_out, ext="png", width=None, height=None):
    os.mkdir(path_out) if not os.path.isdir(path_out) else None
    svg_files = [f for f in os.listdir(path_in)
                 if f.endswith("svg")
                 and os.path.isfile(f"{path_in}/{f}")]
    count = 0
    for svg in svg_files:
        count += 1
        if not width and height:
            size = vg.size(f"{path_in}/{svg}")
        _w = width if width else size[0]
        _h = height if height else size[1]
        fpath_in = f"{path_in}/{svg}"
        fpath_out = f"{path_out}/{svg[:-4]}.{ext}"
        with Image(filename=fpath_in) as image:
            image.format = ext
            if not _w == image.size[0] or _h == image.size[1]:
                image.resize(_w, _h)
            image.save(filename=fpath_out)
        print(f"{count}/{len(svg_files)} | {path_out}/{svg[:-4]}.{ext} "\
              "written to disk")