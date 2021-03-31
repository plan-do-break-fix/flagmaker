from hashlib import md5
import os, sqlite3

import Vector as vg


def run():
    print("Surveying vector graphics...")
    conn = sqlite3.connect(f"/media/flagscraper/survey.sqlite3.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS 'svgs' ("
              "  fname TEXT NOT NULL,"
              "  ncolors INTEGER NOT NULL,"
              "  md5 TEXT NOT NULL"
              ");"
    )
    conn.commit()
    print("Database connection established.")
    count = 0
    for svg in [_f for _f in os.listdir("/media/flagscraper/svg") 
                if _f.endswith("svg")
                and os.path.isfile(f"/media/flagscraper/svg/{_f}")]:
        count +=1
        print(f"Processing file {count} | {svg}")
        with open(f"/media/flagscraper/svg/{svg}", "rb") as _f:
            md5hex = md5(_f).hexdigest()
        ncolors = len(vg.colors(f"/media/flagscraper/svg/{svg}"))
        c.execute("INSERT INTO pngs (fname, md5, ncolors) VALUES (?,?,?)",
                                    (svg, md5hex, ncolors))
        conn.commit()
