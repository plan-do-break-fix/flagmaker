import hashlib, os

import survey.bitmap, filters.bitmap
import survey.vector
import survey.SqliteInterface

def survey(dataset: str, datapath="/media/flagmaker/"):
    path = f"{datapath}/imagesets/{dataset}"
    db = SqliteInterface.Interface(dataset)
    ftypes = get_ftypes(path)    
    if len(ftypes) > 1:
        print("I have not been programmed to do that.")
        return False
    for image in [f for f in os.listdir(path)
                  if os.path.isfile(f) and f.endswith(ftypes[0])]:
        with open(image) as _f:
            md5hash = md5(_f).hexdigest()
        if ftypes[0] in ["bmp", "png", "jpg"]:
            transparency = int(filters.bitmap.no_transparency(path))
            db.record_bitmap(fname, transparency, md5hash)
        elif ftypes[0] == "svg":
            colors = survey.vector.colors(path)
            ncolors = len(colors)
            db.record_svg(fname, ncolors, md5hash, colors)
    



def get_ftypes(path):
    return list(set([i.split(".")[-1] for i in os.listdir(path)]))