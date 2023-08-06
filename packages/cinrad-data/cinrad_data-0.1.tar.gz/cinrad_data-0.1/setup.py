from setuptools import setup, find_packages
from os.path import join
import glob

data_pth = "cinrad_data"

setup(
    name="cinrad_data",
    version="0.1",
    description="Data files for cinrad module",
    long_description="Data files for cinrad module",
    license="MIT Licence",
    author="Puyuan Du",
    author_email="dpy274555447@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="Windows",
    data_files=[
        (join(data_pth, "shapefile"), glob.glob(join(data_pth, "shapefile", "*"))),
        (join(data_pth, "font"), glob.glob(join(data_pth, "font", "*"))),
    ],
)
