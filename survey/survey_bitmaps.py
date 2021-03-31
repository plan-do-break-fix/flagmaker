from hashlib import md5
from PIL import Image
import os, sqlite3


def run():
    print("Surveying bitmaps...")
    conn = sqlite3.connect(f"/media/flagscraper/survey.sqlite3.db")
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
        image = Image.open(f"/media/flagscraper/png/128/{png}").convert("RGBA")
        md5hex = md5(image.tobytes()).hexdigest()
        mean_alpha = sum([i[3] for i in image.getdata()])/len(image.getdata())
        transparency = 0 if mean_alpha == 255 else 1
        if not md5hex and transparency:
            print(f"Error surveying {image}.")
            image.save(f"/media/flagscraper/png/sorted/failure/{png}")
            break
        image.save(f"/media/flagscraper/png/sorted-128/png/{png}") \
            if not transparency \
            else image.save(f"/media/flagscraper/png/sorted-128/transparency/{png}")
        c.execute("INSERT INTO pngs "
                  "  (fname, md5, transparency)"
                  "  VALUES (?,?,?)",
                  (png, md5hex, transparency))
        conn.commit()
