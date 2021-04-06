import sqlite3

BITMAP_SCHEMA = [
    "CREATE TABLE IF NOT EXISTS 'images' ("
    "  fname        TEXT    NOT NULL,"
    "  transparency INTEGER NOT NULL,"
    "  md5          TEXT    NOT NULL"
    ");"
]
SVG_SCHEMA = [
    "CREATE TABLE IF NOT EXISTS 'images' ("
    "  fname   TEXT    NOT NULL,"
    "  ncolors INTEGER NOT NULL,"
    "  md5     TEXT    NOT NULL"
    ");"
    ,
    "CREATE TABLE IF NOT EXISTS 'colors' ("
    "  rgba32 TEXT NOT NULL"
    ");"
    ,
    "CREATE TABLE IF NOT EXISTS 'image_colors' ("
    "  image INTEGER NOT NULL,"
    "  color INTEGER NOT NULL,"
    "  FOREIGN KEY (image) REFERENCES images (rowid),"
    "  FOREIGN KEY (color) REFERENCES colors (rowid)"
    ");"
]


class Interface:

    def __init__(self, dataset: str, datapath="/media/flagmaker"):
        self.conn = sqlite3.connect(f"{datapath}/surveys/{dataset}.sqlite3.db")
        self.c = self.conn.cursor()
        ftype = dataset.split("-")[1].split(".")[0]
        tables = SVG_SCHEMA if ftype == "svg" else BITMAP_SCHEMA
        for table in tables:        
            self.c.execute(table)
        self.conn.commit()

    def record_bitmap(self, fname: str, transparency: int, md5: str) -> bool:
        self.c.execute("INSERT INTO images (fname, transparency, md5) "
                       "VALUES (?,?,?)",
                       (fname, transparency, md5))
        self.conn.commit()
        return True
        
    def record_svg(self, fname: str, ncolors: int, md5: str,
                   colors: list) -> bool:
        if self.image_exists(fname):
            print(f"Image {fname} already exists.")
            return True
        self.c.execute("INSERT INTO images (fname, ncolors, md5) "
                       "VALUES (?,?,?)",
                       (fname, ncolors, md5))
        self.conn.commit()
        image_pk = self.c.lastrowid
        for color in colors:
            if self.color_exists(color):
                print(f"Color {color} already exists.")
                break
            self.c.execute("INSERT INTO colors (rgba32) VALUES (?)", (color,))
            color_pk = self.c.lastrowid
            self.c.execute("INSERT INTO image_colors (image, color) "
                           "VALUES (?, ?)", (image_pk, color_pk))
            self.conn.commit()
            return True
        
    def image_exists(self, fname: str) -> bool:
        self.c.execute("SELECT rowid FROM images WHERE fname=?", (fname,))
        return True if self.c.fetchone() else False

    def color_exists(self, color: str) -> bool:
        self.c.execute("SELECT rowid FROM colors WHERE rgba32=?", (color,))
        return True if self.c.fetchone() else False

        