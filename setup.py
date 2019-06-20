from setuptools import find_packages, setup

requires = ["numpy", "Cartopy", "richdem", 
    "matplotlib", "elevation", "click==6.7", "scipy"]

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='Automated method to extract river profiles using GRASS GIS',
    author='Carla Pont',
    author_email='c.pont17@imperial.ac.uk',
    url="https://grass-gis-to-extract-river-profiles.readthedocs.io",
    license='MIT',
    scripts = ['bin/extract-rivers'],
    entry_points = {
            "console_scripts": [
                "visualise = grass_river_extraction_tools.visualise_dem:main"
            ]
    },
    install_requires=requires,
    python_requires='~=3.6'
)
