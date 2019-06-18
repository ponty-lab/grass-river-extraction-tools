Grass River Extraction Tools
============================

A command-line tool to automatically extract river profiles 
from digital elevation models using GDAL and GRASS GIS.


Prerequisites
-------------

-  Python 2 or 3
-  Sphinx 2.1.1 - This can be installed with pip or conda depending on how you
   manage your Python packages

.. code:: bash

   $ sudo apt install python3-sphinx or sudo apt install python-sphinx
   $ sudo pip install sphinx

-  GRASS GIS 7.6

.. code:: bash
   $ sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
   $ sudo apt-get update
   $ sudo apt-get install grass

Getting Started
---------------

Install and eexecute the project locally into your $HOME/bin directory. If you
don't already have a bin directory for your bash scripts, create one
to store your bash scripts.

**Documentation.** For more information, read the step by step guide on
using GDAL and GRASS GIS to extract river profiles. 

https://grass-gis-to-extract-river-profiles.readthedocs.io/en/latest/


Example usage
~~~~~~~~~~~~~

.. code:: bash

   $ extract-rivers

::

   An automated method to extract rivers using GRASS GIS

   Usage: ./../grass-river-extraction-tools-v1/extract_rivers.sh [OPTIONS] -d <grassdir> -f <dem> -s <shapefile> -t <threshold>

   ARGUMENTS
   	-d | --grassdir		GRASS PROJECT directory
   	-f | --dem		    Filled DEM to upload
   	-s | --shapefile	Shapefile to mask DEM
   	-t | --threshold	minimum catchment size (pixels)
   OPTIONS
   	-o | --overwrite	Overwrite existing files
   	-h | --help		help


Contribute!
-----------

Please contribute! Use `Github Flow <https://guides.github.com/introduction/flow/index.html>`_ to suggest changes.

- Fork the repo and create your branch in master - send me pull requests.

- Documentation uses `Python-Sphinx <http://www.sphinx-doc.org/en/master/>`_ and `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ syntax

::

   Project Organization
   ------------

      ├── LICENSE
      ├── Makefile           <- Makefile with commands like `make data`
      ├── README.md          <- The top-level README for developers using this project.
      ├── data
      │   ├── external       <- Data from third party sources.
      │   ├── interim        <- Intermediate data that has been transformed.
      │   ├── processed      <- The final, canonical data sets for modeling.
      │   └── raw            <- The original, immutable data dump.
      │
      ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
      │
      ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
      │                         generated with `pip freeze > requirements.txt`
      │
      ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
      ├── src                <- Source code for use in this project.
      │   ├── __init__.py    <- Makes src a Python module
      │   │
      │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
      │       └── visualize.py
      │
      └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org
      
--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
=======

