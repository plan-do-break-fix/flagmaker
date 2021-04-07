#!/bin/python3
# transform.color v0.1
from wand.color import Color
from wand.image import Image, IMAGE_TYPES
from wand.exceptions import ImageError


def image_type(fpath_in, path_out,
               image_type=None,
               quantize=0,
               write_safe=True
               ) -> None:
    """
    Convert bitmap type, optionally quantize image colors.
    
    :param fpath_in: path of bitmap to transform
    :param path_out: directory for transformed image
    :param image_type: ImageMagick Image Type to convert image to (default None)
    :param quantize: non-zero number of colors to quantize output to (default 0)
    :param write_safe: do not write over existing files (default True)
    :returns None: output is image file
    :raises RuntimeError: if image_type is not a valid ImageMagick Image Type
    :raises RuntimeError: if write safety enabled and output file exists
    :raises ImageError: if ImageError returned by MagickWand
    """
    if image_type and image_type not in IMAGE_TYPES:
        print(f"{image_type} is not a recognized ImageMagick Image Type.")
        raise RuntimeError
    fpath_out = f"{path_out}/{fpath_in.split('/')[-1]}"
    if write_safe and os.path.isfile(fpath_out):
        raise RuntimeError
    try:
        with Image(filename=fpath_in) as image:
            if quantize:
                image.quantize(number_colors=quantize)
            if image_type and image_type != image.type:
                image.type = image_type
            image.save(filename=fpath_out)
            image.close()
    except ImageError:
        print("Unable to convert image.")
        return None


def apply_palette():
    pass

