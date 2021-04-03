#!/bin/python3
import os, shutil
from wand.color import Color
from wand.image import Image, IMAGE_TYPES
from wand.exceptions import ImageError

def rasterize(path_in, path_out,
              width=None, height=None,
              ext="png",
              image_type="truecolor",
              preserve_alpha=True,
              background="white",
              quantize=0,
              write_safe=True
              ) -> None:
    """
    Wrapper wrapper for consistent, repeatable batch rasterization operations.

    :param path_in: directory containing the svg files to rasterize
    :param path_out: directory for output rasterized images
    :param width: width in pixels if output image is to be scaled horizontally
    :param height: height in pixels if output image is to be scaled vertically 
    :param ext: file format for output (default 'png')
    :param image_type: ImageMagick image type (default 'truecolor')
    :param preserve_alpha: allow transparent pixels in output (default True)
    :param background: color to use for transparent pixels (default 'white')
    :param quantize: number of colors to quantize output to if not 0 (default 0)
    :param write_safe: do not write over existing files (default True)
    :returns None: inteded for batch processing; output is image files
    :raises RuntimeError: if non-existent Image Type passed as image_type
    :raises ImageError: if ImageError returned by MagickWand
    """
    os.mkdir(path_out) if not os.path.isdir(path_out) else None
    if image_type not in IMAGE_TYPES:
        print(f"{imgtype} is not a recognized ImageMagick Image Type.")
        raise RuntimeError
    svg_files = [f for f in os.listdir(path_in)
                 if f.endswith("svg")
                 and os.path.isfile(f"{path_in}/{f}")]
    count = 0  # used only for displaying progress to stdout
    for svg in svg_files:
        count += 1
        fpath_out = f"{path_out}/{svg[:-4]}.{ext}"
        if write_safe and os.path.isfile(fpath_out):
            print(f"File {count}/{len(svg_files)} already exists.")
            break
        fpath_in = f"{path_in}/{svg}"
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
                    if quantize:
                        image.quantize(number_colors=quantize)
                    if image_type:
                        image.type = image_type
                    image.save(filename=fpath_out)
                    image.close()
        except ImageError:
            os.mkdir(f"{path_in}/bad_raster/") \
                    if not os.path.isdir(f"{path_in}/bad_raster/") else None
            print(f"Unable to rasterize {count}/{len(svg_files)} {svg}")
            shutil.move(fpath_in, f"{path_in}/bad_raster/")
        print(f"{count}/{len(svg_files)} {path_out}/{svg[:-4]}.{ext} "\
              "written to disk")