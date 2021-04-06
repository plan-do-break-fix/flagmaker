import hashlib, os

import survey.bitmap as bitmap 
import survey.vector as vector
from survey import SqliteInterface

def survey(dataset: str, datapath="/media/flagmaker"):
    path = f"{datapath}/imagesets/{dataset}"
    print(path)
    db = SqliteInterface.Interface(dataset)
    ftypes = get_ftypes(path)
    print(f"Found {ftypes[0]} files.")    
    if len(ftypes) > 1:
        print("I have not been programmed to do that.")
        return False
    for image in [f for f in os.listdir(path)
                  if os.path.isfile(f"{path}/{f}") and f.endswith(ftypes[0])]:
        print(f"Processing {image}")
        fpath = f"{path}/{image}"
        with open(fpath, "rb") as _f:
            md5hash = hashlib.md5(_f.read()).hexdigest()
        if ftypes[0] in ["bmp", "png", "jpg"]:
            mean_alpha = bitmap.channel_mean(fpath, "a")
            transparency = 0 if mean_alpha == 255.0 else 1
            db.record_bitmap(image, transparency, md5hash)
        elif ftypes[0] == "svg":
            colors = vector.colors(fpath)
            ncolors = len(colors)
            db.record_svg(image, ncolors, md5hash, colors)


def get_ftypes(path):
    return list(set([i.split(".")[-1] for i in os.listdir(path)]))
