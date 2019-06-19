Grass River Extraction Tools
============================

A command-line tool to automatically extract river profiles 
from digital elevation models using GDAL, Richdem and GRASS GIS.

Prerequisites
-------------

Install the following packages, if you don't already have them.

-  Python 2 or 3

-  GRASS GIS 7.6

.. code:: bash

   $ sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
   $ sudo apt-get update
   $ sudo apt-get install grass

Installation
------------

To create a virtual environment:

.. code:: bash

   $ python3 -m venv test.env 
   $ . test.venv/bin/activate

Once the packages have been installed, clone the tools from here and 
install the local package: 

.. code:: bash

   $ git clone git@github.com:pontc/grass-river-extraction-tools.git
   $ pip install -e extract-rivers
   $ extract-rivers --help

   An automated method to extract rivers using GRASS GIS

   Usage: ./../grass-river-extraction-tools-v1/extract_rivers.sh [OPTIONS] -d <grassdir> -f <dem> -s <shapefile> -t <threshold>

   ARGUMENTS
   	-d | --grassdir		GRASS PROJECT directory
   	-f | --dem		   Filled DEM to upload
   	-s | --shapefile	Shapefile to mask DEM
   	-t | --threshold	minimum catchment size (pixels)
   OPTIONS
   	-o | --overwrite	Overwrite existing files
   	-h | --help		help


Documentation
---------------

For more information, read the step by step guide on
using GDAL, Richdem and GRASS GIS to extract river profiles. 

https://grass-gis-to-extract-river-profiles.readthedocs.io/en/latest/

Tutorials
---------

Instructions on how to use the river extraction with an example datset is
available in the `Example directory <https://github.com/pontc/grass-river-extraction-tools/tree/master/Example>`_.


Contribute!
-----------

Please contribute! Use `Github Flow <https://guides.github.com/introduction/flow/index.html>`_ to suggest changes.

- Fork the repo and create your branch in master - send me pull requests.

- Documentation uses `Python-Sphinx <http://www.sphinx-doc.org/en/master/>`_ and `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ syntax
