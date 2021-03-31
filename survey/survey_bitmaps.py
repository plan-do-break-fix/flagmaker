from hashlib import md5
from PIL import Image
import os, sqlite3

import Bitmap as bmp


def run():
    print("Surveying bitmaps...")
    conn = sqlite3.connect(f"survey.sqlite3.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS 'pngs' ("
              "  fname TEXT NOT NULL,"
              "  meanR INTEGER NOT NULL,"
              "  meanB INTEGER NOT NULL,"
              "  meanG INTEGER NOT NULL,"
              "  modeR INTEGER NOT NULL,"
              "  modeB INTEGER NOT NULL,"
              "  modeG INTEGER NOT NULL,"
              "  transparency INTEGER NOT NULL,"
              "  ncolors INTEGER NOT NULL,"
              "  md5 TEXT NOT NULL"
              ");"
    )
    c.execute("CREATE TABLE IF NOT EXISTS 'colors' ("
              "  rgba32 TEXT NOT NULL);"
    )
    c.execute("CREATE TABLE IF NOT EXISTS 'image_colors' ("
              "  image INTEGER NOT NULL,"
              "  color INTEGER NOT NULL,"
              "  FOREIGN KEY (image) REFERENCES pngs (rowid),"
              "  FOREIGN KEY (color) REFERENCES colors (rowid)"
              ");"
    )
    conn.commit()
    print("Database connection established.")
    count = 0
    for png in [_f for _f in os.listdir("/media/flagscraper/png/128") 
                if _f.endswith("png")
                and os.path.isfile(f"/media/flagscraper/png/128/{_f}")]:
        count +=1
        print(f"Processing file {count} | {png}")
        image = Image.open(f"/media/flagscraper/png/128/{png}")
        md5hex = md5(image.tobytes()).hexdigest()
        pixels = image.all_pixels(image)
        avg = bmp.composite_mean(pixels)
        mode = bmp.composite_mode(pixels)      
        transparency = 0 if avg[3] == 255 else 1
        avg = [round(a) for a in avg]
        if not transparency:
            color_tuples = image.getcolors()
            if not color_tuples:
                ncolors = 0 # Zero colors = Over 256 colors
            else:
                color_list = []
                for _c in image.getcolors():
                    rgba32 = "#{:02x}{:02x}{:02x}{:02x}"\
                             .format(_c[1][0], _c[1][1], _c[1][2], 255)
                    if rgba32 not in color_list:
                        color_list.append(rgba32)
                ncolors = len(color_list)
                for _i, _color in enumerate(color_list):
                    c.execute("SELECT rowid FROM colors WHERE rgba32=?",
                              (_color,))
                    color_pk = c.fetchone()
                    if not color_pk:
                        c.execute("INSERT INTO colors (rgba32) VALUES (?)",
                                  (_color,))
                        conn.commit()
                        color_pk = c.lastrowid
                    color_list[_i] = (_color, color_pk)
        if not md5hex and avg and mode and transparency and ncolors:
            print(f"Error surveying {image}.")
            image.save(f"./sorted/failure/{png}")
            break
        image.save("./sorted-128/png/{png}") \
            if not transparency \
            else image.save("./sorted-128/transparency/{png}")
        c.execute("INSERT INTO pngs "
                  "  (fname, md5,"
                  "   meanR, meanB, meanG, "
                  "   modeR, modeB, modeG, "
                  "   transparency, ncolors)"
                  "  VALUES (?,?,?,?,?,?,?,?,?)",
                  (image, md5hex, avg[0], avg[1], avg[2],
                   mode[0], mode[1], mode[2], transparency, ncolors))
        image_pk = c.lastrowid
        for _color in color_list:
            c.execute("INSERT INTO image_colors (image, color) VALUES (?,?)",
                      (image_pk, _color[1]))
        conn.commit()
