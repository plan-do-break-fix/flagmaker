import re
from typing import List, Tuple
import xml.etree.ElementTree as Tree
from xml.etree.ElementTree import Element


def load_xml(fpath: str) -> Element:
    return Tree.parse(fpath).getroot()


def size(root: Element) -> Tuple[int]:
    w, h = root.attrib["width"], root.attrib["height"]
    if not h or not w:
        raise ValueError
    return (w, h) 


def colors(fpath: str) -> List[str]:
    """
    Return list of all colors used in file."""
    with open(fpath) as _f:
        svg = _f.read()
    colors = list(set(re.findall('#[0-9a-fA-F]{3,6}', svg)))
    return colors if "#fff" not in colors \
        else [i for i in colors if i != "#fff"] + ["#FFFFFF"]


