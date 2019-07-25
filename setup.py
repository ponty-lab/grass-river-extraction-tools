import sys
import subprocess
from setuptools import find_packages, setup


def gdal_warning(msg=None):
    raise Exception(f"Unable to determine gdal version using gdal-config: {msg}")


def libgdal_version():
    version = None
    try:
        proc = subprocess.Popen(['gdal-config', '--version'], stdout=subprocess.PIPE)
        version = proc.stdout.read().decode('utf-8').rstrip()
        if not version:
            gdal_warning("Version not set")
    except Exception as e:
        gdal_warning(e)
    return f"{version}.*"


requires = ["numpy", "Cartopy", "richdem",
            "matplotlib", "elevation", "click<7", "scipy",
            "pygdal=="+libgdal_version(), "tqdm",]

setup(
    name='grass_river_extraction_tools',
    packages=find_packages(),
    version='0.1.3',
    description='Automated method to extract river profiles using GRASS GIS',
    author='Carla Pont',
    author_email='c.pont17@imperial.ac.uk',
    url="https://grass-gis-to-extract-river-profiles.readthedocs.io",
    license='MIT',
    scripts=['bin/extract-rivers'],
    entry_points={
            "console_scripts": [
                "visualise = grass_river_extraction_tools.visualise_dem:main"
            ]
    },
    install_requires=requires,
    python_requires='~=3.6'
)
