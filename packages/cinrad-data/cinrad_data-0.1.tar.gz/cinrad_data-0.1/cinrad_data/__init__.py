import os

current_dir, _ = os.path.split(__file__)
SHP_DIR = os.path.join(current_dir, "shapefile")
FONT_DIR = os.path.join(current_dir, "font")


def get_font_path():
    return os.path.join(FONT_DIR, "NotoSansHans-Regular.otf")


def get_shp_list():
    return [os.path.join(SHP_DIR, i) for i in ["County", "City", "Province"]]


def get_shp_file(name):
    return os.path.join(SHP_DIR, name)
