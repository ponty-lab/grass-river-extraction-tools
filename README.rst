Grass River Extraction Tools
============================

A command-line tool to automatically extract river profiles 
from digital elevation models using GDAL, Richdem and GRASS GIS.

Prerequisites
-------------

Install the following packages, if you don't already have them.

-  Python 3.6 or greater

-  GRASS GIS 7.6

.. code:: bash

   $ sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
   $ sudo apt-get update
   $ sudo apt-get install grass

- GDAL

.. code:: bash

    sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
    sudo apt-get update
    sudo apt-get install gdal-bin
    sudo apt-get install libgdal-dev

Installation
------------

To create a virtual environment, replace *tmp* with the name of your env:

.. code:: bash

   $ python3 -m venv test.env 
   $ . test.venv/bin/activate

Once pre-requisites have been installed, clone the local package 
from here and install: 

.. code:: bash

   $ git clone git@github.com:pontc/grass-river-extraction-tools.git
   $ pip install -e grass-river-extraction-tools

Now finish up the GDAL installation, run this after pip installing
the local packages to avoid errors (fingers crossed it works, its a 
bit fiddly!)

.. code:: bash

    pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal" 

Launch GRASS GIS and enable the following extensions:

.. code:: bash

   GRASS :~ > g.extension r.stream.extract r.stream.basins

Quick Start
-----------

To extract rivers from GRASS GIS, run:

.. code:: bash

   $ extract-rivers --help

   An automated method to extract rivers using GRASS GIS

   Usage: ./../grass-river-extraction-tools-v1/extract_rivers.sh [OPTIONS] -p <grassdir> -d <dem> -s <shapefile> -t <threshold>

   ARGUMENTS
   	-p | --grassdir		GRASS PROJECT directory
   	-d | --dem		   Filled DEM to upload
   	-s | --shapefile	Shapefile to mask DEM
   	-t | --threshold	minimum catchment size (pixels)
   OPTIONS
    -n | --number           Number of rivers to extract. Default: All
   	-o | --overwrite	Overwrite existing files
   	-h | --help		help

To check river extraction, run the visualisation tool:

.. code:: bash

    $ visualise --help

    Usage: visualise [OPTIONS]

    Simple tool to visualise River Extraction

    Options:
    --name TEXT       Name of region  [required]
    --dem TEXT        Name of lat/lng DEM  [required]
    --directory TEXT  Output directory  [required]
    --river TEXT      River file  [required]
    --help            Show this message and exit.


Documentation
---------------

For more information, read the `step by step guide <https://grass-gis-to-extract-river-profiles.readthedocs.io/en/latest/>`_ on
using GDAL, Richdem and GRASS GIS to extract river profiles. 

https://grass-gis-to-extract-river-profiles.readthedocs.io/en/latest/

Tutorials
---------

A simple tutorial on how to use the river extraction with an example datset is
available in the `Example directory <https://github.com/pontc/grass-river-extraction-tools/tree/master/Example>`_.


Contribute!
-----------

Please contribute! Use `Github Flow <https://guides.github.com/introduction/flow/index.html>`_ to suggest changes.

- Fork the repo and create your branch in master - send me pull requests.

- Documentation uses `Python-Sphinx <http://www.sphinx-doc.org/en/master/>`_ and `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ syntax
