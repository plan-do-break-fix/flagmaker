

def basename(fpath):
    """Return file name w/o extension or folder name if fpath is a directory."""
    if fpath.endswith("/") and len(fpath) > 1:
        return fpath.split("/")[-2]
    fname = fpath.split("/")[-1]
    return ".".join(fname.split(".")[:-1])