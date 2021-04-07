#!/bin/python3
import os

from pipelines.Pipeline import AbstractPipeline
from survey.SqliteInterface import Interface as SqliteInterface
from transforms import color
from transforms.rasterize import rasterize


class Pipeline(AbstractPipeline):

    def __init__(self, datapath="/media/flagmaker"):
        super().__init__(datapath=datapath)
        self.input = "wikipedia.2021.03-svg.raw"
        self.output = "wikipedia.2021.03-png.simple:grayscale.128"
        self.svg_db = SqliteInterface(self.input)
        self.png_db = SqliteInterface("wikipedia.2021.03-png.survey:128")

    def process(self):
        os.makedirs(f"{self.datapath}/imagesets/{self.output}")
        while self.to_process:
            image = self.to_process.pop()
            print(f"Processing {image}")
            ncolors = self.svg_db.get_ncolors(image)
            if ncolors < 6:
                rasterize(fpath_in=f"{self.datapath}/imagesets/{self.input}/{image}", 
                        path_out=f"{self.datapath}/imagesets/{self.output}",
                        width=128, height=64,
                        preserve_alpha=False)
                color.image_type(fpath_in=f"{self.datapath}/imagesets/{self.output}/{'.'.join(image.split('.')[:-1])}.png",
                                 path_out=f"{self.datapath}/imagesets/{self.output}",
                                 image_type="grayscale",
                                 quantize=ncolors,
                                 write_safe=False) 
