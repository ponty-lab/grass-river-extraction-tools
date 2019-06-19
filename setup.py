from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='Automated method to extract river profiles using GRASS GIS',
    author='Carla Pont',
    author_email='c.pont17@imperial.ac.uk',
    url="https://grass-gis-to-extract-river-profiles.readthedocs.io",
    license='MIT',
    scripts = ['bin/extract-rivers', 'bin/process-rivers'],
    entry_points = {
            'console_scripts': ["visualise = src.visualise_dem:plot"]
    }
)
