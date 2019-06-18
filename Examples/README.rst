Quickstart
==========

A command-line tool to automatically extract river profiles 
from digital elevation models using GDAL and GRASS GIS.

Getting data
-------------

To test this package, we'll need to download a dataset. To do this we can use
`Elevation <https://pypi.org/project/elevation/>`_ to easily download an SRTM dataset. Otherwise, use your own merged dataset.

Install the latest version of `Elevation <https://pypi.org/project/elevation/>`_ and any dependencies not installed:

.. code:: bash

   $ pip install elevation

Download NASA's `SRTM 30m Global 1 arc second V003 <https://search.earthdata.nasa.gov/search>`_ for your area of interest. In this example,
we are downloading tiles covering the Central Apennines in Italy.

.. code:: bash

   $ eio clip -o Apennines_30m_DEM.tif --bounds 12 41 14 44

Parameters
-----------

::

   An automated method to extract rivers using GRASS GIS

   Usage: ./../grass-river-extraction-tools-v1/extract_rivers.sh [OPTIONS] -d <grassdir> -f <dem> -s <shapefile> -t <threshold>

   ARGUMENTS
      -d | --project       GRASS PROJECT name
      -f | --dem		      Filled DEM to upload
      -p | --projection    Projection
      -s | --shapefile	   Shapefile to mask DEM
      -t | --threshold	   minimum catchment size (pixels)
   OPTIONS
      -n | --rivers        Number of rivers: default all
      -o | --overwrite	   Overwrite existing files
      -h | --help		      help


The code will extract a stream network for a given threshold using a single
flow direction based on the D8 method. 

-  *Shapefile*
   A high resolution GSHSS coastline is provided within the directory 'data'

-  *Projection*
   Here we use an equal areas projection, Lamber Conformal Conic for Europe.
   Choose an equal areas projection, note that the Central Apennines straddles
   2 UTM zones.

-  *Threshold*
   We use a 300 pixel threshold, equivalent to a drainage area of 
   0.27 km\ :sup:`2` for the 30 m DEM. This will determine the drainage density, 
   a higher threshold value will reduce drainage density. 
   
-  *No of rivers* The default is to extract all rivers in the stream network.
   For this example, we will limit the extraction to 50 rivers.

Depression Filling method
^^^^^^^^^^^^^^^^^^^^^^^^^

While GRASS GIS does not strictly require the DEM to be filled for channel 
extraction (See documentation for dicussion on handling depressions), this
method uses Richdem's depression filling tool based on Barnes et al. (2016) priority-flood algorithm.

Running River Extraction
-------------------------

Example usage
~~~~~~~~~~~~~

.. code:: bash

   $ extract-rivers -d Italy -p ESPG:3034 -f Apennines_30m_DEM.tif 
   -s data/GSHHS_h_L1.shp -t 300 -n 50


Visualisation
-------------

River outputs can be visualised by running:

.. code:: bash

   $ visualise-dem






