
from rasterize import rasterize
from survey import survey_bitmaps
from survey import survey_vectors

def run():
    survey_vectors.run()
    rasterize("/media/flagscraper/svg",
              "/media/flagscraper/png/128",
              ext="png",
              width=128, height=64)
    survey_bitmaps.run()
