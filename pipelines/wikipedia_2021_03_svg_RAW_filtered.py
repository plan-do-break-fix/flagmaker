#!/bin/python3
import os

from pipelines.Pipeline import AbstractPipeline
from transforms.rasterize import rasterize


class Pipeline(AbstractPipeline):

    def __init__(self, datapath="/media/flagmaker"):
        super().__init__(datapath="/media/flagmaker")
        self.input = "wikipedia.2021.03-svg.RAW"
        self.output = "wikipedia.2021.03-png.survey:128"

    def process(self):
        os.makedirs(f"{datapath}/{self.output}")
        while self.to_process:
            image = self.to_process.pop()
            print(f"Processing {image}")
            rasterize(fpath_in=f"{datapath}/{self.input}/{image}", 
                      path_out=f"{datapath}/{self.output}",
                      width=128, height=64)
        self.survey(self.output)






