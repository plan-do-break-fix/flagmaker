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
    c.execute("CREATE TABLE IF NOT EXISTS 'colors' ("
              "  rgba32hex TEXT NOT NULL);"
    )
    c.execute("CREATE TABLE IF NOT EXISTS 'svg_colors' ("
              "  svg INTEGER NOT NULL,"
              "  color INTEGER NOT NULL,"
              "  FOREIGN KEY (svg) REFERENCES svgs (rowid),"
              "  FOREIGN KEY (color) REFERENCES colors (rowid)"
              ");"
    )
    conn.commit()
    print("Database connection established.")
    count = 0
    for svg in [_f for _f in os.listdir("/media/flagscraper/svg") 
                if _f.endswith("svg")
                and os.path.isfile(f"/media/flagscraper/svg/{_f}")]:
        count +=1
        c.execute("SELECT rowid FROM svgs WHERE fname=?", (svg))
        if c.fetchone():
            print(f"Skipping file {count} | {svg}")
            break
        print(f"Processing file {count} | {svg}")
        with open(f"/media/flagscraper/svg/{svg}") as _f:
            data = _f.read()
        md5hex = md5(data.encode()).hexdigest()
        color_list = vg.colors(f"/media/flagscraper/svg/{svg}")
        ncolors = len(color_list)
        c.execute("INSERT INTO svgs (fname, md5, ncolors) VALUES (?,?,?)",
                                    (svg, md5hex, ncolors))
        svg_pk = c.lastrowid
        for color in color_list:
            c.execute("SELECT rowid FROM colors WHERE rgba32hex=?", (color,))
            color_pk = c.fetchone()
            if not color_pk:
                c.execute("INSERT INTO colors (rgba32hex) VALUES (?)", (color,))
                color_pk = c.lastrowid
            c.execute("INSERT INTO svg_colors (svg, color) VALUES (?,?)",
                                              (svg_pk, color_pk))
            conn.commit()
