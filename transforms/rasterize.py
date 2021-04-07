#!/bin/python3
# transform.rasterize v0.1
import os, shutil
from wand.color import Color
from wand.image import Image, IMAGE_TYPES
from wand.exceptions import ImageError


def rasterize(fpath_in, path_out,
              width, height,
              ext="png",
              preserve_alpha=True,
              background="white",
              write_safe=True
              ) -> None:
    """
    Produce rasterized bitmap from scalable vector graphic.

    :param fpath_in: path of svg to rasterize
    :param path_out: directory for rasterized image
    :param width: desired width in pixels of output image
    :param height: desired height in pixels of output image 
    :param ext: file format for output (default 'png')
    :param preserve_alpha: allow transparent pixels in output (default True)
    :param background: used when not preserving alpha (default 'white')
    :param write_safe: will not write over existing files (default True)
    :returns None: output is rasterized image file
    :raises RuntimeError: if write safety would be violated
    :raises ImageError: if ImageError is returned by MagickWand
    """
    fpath_out = f"{path_out}/{fpath_in.split('/')[-1][:-4]}.{ext}"
    if write_safe and os.path.isfile(fpath_out):
        raise RuntimeError
    try:
        if preserve_alpha:
            with Image(filename=fpath_in, background="transparent") as image:
                image.resize(width, height)
                image.save(filename=fpath_out)
        else:
            with Image(filename=fpath_in) as image:
                with image.convert(ext) as converted:
                    converted.background_color = background
                    converted.alpha_channel = "deactivate"
                    converted.resize(width, height)
                    converted.save(filename=fpath_out)
    
    except ImageError:
        print(f"Unable to rasterize {svg}.")
    print(f"{fpath_out} written to disk.")