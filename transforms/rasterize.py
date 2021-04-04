#!/bin/python3
# transform.rasterize v0.1
import os, shutil
from wand.color import Color
from wand.image import Image, IMAGE_TYPES
from wand.exceptions import ImageError


def rasterize(fpath_in, path_out,
              width=None, height=None,
              ext="png",
              preserve_alpha=True,
              background="white",
              write_safe=True
              ) -> None:
    """
    Produce rasterized bitmap from scalable vector graphic.

    :param fpath_in: path of svg to rasterize
    :param path_out: directory for rasterized image
    :param width: width in pixels if output image is to be scaled horizontally
    :param height: height in pixels if output image is to be scaled vertically 
    :param ext: file format for output (default 'png')
    :param preserve_alpha: allow transparent pixels in output (default True)
    :param background: color to use for transparent pixels (default 'white')
    :param write_safe: do not write over existing files (default True)
    :returns None: output is image file
    :raises RuntimeError: if write safety enabled and output file exists
    :raises ImageError: if ImageError returned by MagickWand
    """
    fpath_out = f"{path_out}/{fpath_in.split("/")[-1][:-4]}.{ext}"
    if write_safe and os.path.isfile(fpath_out):
        raise RuntimeError
    try:
        with Image(filename=fpath_in) as image:
            image.background_color = "transparent" if preserve_alpha \
                                        else background
            if width != image.size[0] or height != image.size[1]:
                image.resize(width, height)
            image.save(filename=fpath_out)
            image.close()
        if quantize or image_type != "truecolor":
            with Image(filename=fpath_out) as image:
    except ImageError:
        print(f"Unable to rasterize {svg}")
    print(f"{count}/{len(svg_files)} {path_out}/{svg[:-4]}.{ext} "\
            "written to disk")