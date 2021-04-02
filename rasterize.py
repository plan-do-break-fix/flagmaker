import os, shutil
from wand.color import Color
from wand.image import Image, IMAGE_TYPES
from wand.exceptions import ImageError

def rasterize(path_in, path_out,
              width=None, height=None,
              ext="png",
              imgtype="truecolor",
              preserve_alpha=True,
              background="white",
              quantize=0,
              writesafe=True
              ) -> None:
    """Batch rasterization method.

    Keyword arguments:
    path_in -- directory containing the svg files to rasterize
    path_out -- directory for output rasterized images
    width -- width in pixels if output image is to be scaled horizontally
    height -- height in pixels if output image is to be scaled vertically 
    ext -- file format for output (default 'png')
    imgtype -- ImageMagick image type (default 'truecolor')
    preserve_alpha -- allow transparent pixels in output (default True)
    background -- color to use for transparent pixels (default 'white')
    quantize -- if > 0, number of colors to restrict output to (default 0)
    writesafe -- if True, will not write over existing files (default True)
    """
    os.mkdir(path_out) if not os.path.isdir(path_out) else None
    if imgtype not in IMAGE_TYPES:
        print(f"{imgtype} is not a recognized ImageMagick Image Type.")
        raise RuntimeError
    svg_files = [f for f in os.listdir(path_in)
                 if f.endswith("svg")
                 and os.path.isfile(f"{path_in}/{f}")]
    count = 0  # used only for stdout progress display
    for svg in svg_files:
        count += 1
        fpath_out = f"{path_out}/{svg[:-4]}.{ext}"
        if writesafe and os.path.isfile(fpath_out):
            print(f"File {count}/{len(svg_files)} already exists.")
            break
        fpath_in = f"{path_in}/{svg}"
        try:
            with Image(filename=fpath_in) as image:
                image.background_color = "transparent" if preserve_alpha \
                                         else background
                image.type = imgtype
                if width != image.size[0] or height != image.size[1]:
                    image.resize(width, height)
                image.save(filename=fpath_out)
                image.close()
            if quantize:
                with Image(filename=fpath_out) as image:
                    image.quantize(number_colors=quantize)
                    image.save(filename=fpath_out)
        except ImageError:
            print(f"Unable to rasterize {svg}")
            shutil.move(fpath_in, "/media/flagscraper/failed-rasterization/")
        print(f"{count}/{len(svg_files)} {path_out}/{svg[:-4]}.{ext} "\
              "written to disk")