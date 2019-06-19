Quickstart
===========

Project organisation
--------------------

This uses the project structure is based on the philosophy of `Cookiecutter Data 
Science <https://github.com/drivendata/cookiecutter-data-science>`_: *A logical, reasonably standardized, but flexible project structure for doing and sharing data science work*.

::

   ├── Example.rst      <- Quick start instructions to run river extraction.
   ├── data 
   │   ├── external     <- Third party data.
   │   ├── interim      <- Sorted river data
   │   ├── processed    <- The final, canonical data sets for modeling.
   │   └── raw          <- The original, immutable data dump (GRASS river data)
   ├── figures          <- Example of figures to visualise the process.

Getting data
-------------

To test this package, we'll need to download a dataset. To do this we can use
`Elevation <https://pypi.org/project/elevation/>`_ to obtain an `SRTM 30m Global 1 arc second V003 dataset <https://search.earthdata.nasa.gov/search>`_. Otherwise, use your own dataset.

In this example, we download tiles covering the region of the Central Apennines in Italy into the *data/external* directory.

.. code:: bash

   $ eio clip -o data/external/Apennines_30m_DEM.tif --bounds 12 41 14 44

Projecting DEM
--------------

Before running *extract-rivers* programme, make sure your DEM is projected into 
a suitable equal areas projection.

.. code:: bash

   $ gdalwarp -t_srs 
   "+proj=lcc +lat_0=52 +lon_0=10 +lat_1=35 +lat_2=65 +ellps=GRS80 +units=m +no_defs" 
   data/external/Apennines_30m_DEM.tif data/external/Apennines_30m_DEM_LCC.tif

Running River Extraction
========================

The programme will extract a stream network using a given drainage 
area threshold based on D8 method for single flowd irection. 

**Depression Filling method**

While GRASS GIS does not strictly require the DEM to be filled for channel 
extraction (see documentation for further discussion on handling depressions), this
fills the DEM using Richdem's depression filling tool based on Barnes et al. (2016)
priority-flood algorithm.

Parameters
----------
::
   
   $ extract-rivers --help
   
   An automated method to extract rivers using GRASS GIS

   Usage: ./../grass-river-extraction-tools-v1/extract_rivers.sh [OPTIONS] 
   -d <grassdir> -f <dem> -s <shapefile> -t <threshold>
 
   ARGUMENTS
      -d | --project       GRASS PROJECT name
      -f | --dem		      Projected DEM to upload
      -s | --shapefile	   Shapefile to mask DEM
      -t | --threshold	   minimum catchment size (pixels)
   OPTIONS
      -n | --rivers        Number of rivers to extract. Default: All
      -o | --overwrite	   Overwrite existing files
      -h | --help		      help


- *Shapefile*: A high resolution GSHSS coastline is provided within the directory 'data/external'

- *Projection*: Choose an equal areas projection. Here we use an equal areas projection, Lamber Conformal Conic for Europe as the Central Apennines straddles two different UTM zones.

- *Threshold*: We use a 300 pixel threshold, equivalent to a drainage area of 
  0.27 km\ :sup:`2` for the 30 m DEM. This will determine the drainage density, 
  a higher threshold value will reduce drainage density. 
   
- *No of rivers* The default is to extract all rivers in the stream network.
  For this example, we will limit the extraction to 50 rivers.
 
Example usage
-------------

.. code:: bash

   $ extract-rivers -d grass -p ESPG:3034 
   -f data/external/Apennines_30m_DEM_LCC.tif -s data/external/GSHHS_h_L1.shp 
   -t 300 -n 50


Visualisation
-------------

River outputs can be visualised by running:

.. code:: bash

   $ visualise-dem

