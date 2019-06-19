Quickstart
===========

Getting data
-------------

To test this package, we'll need to download a dataset. To do this we can use
`Elevation <https://pypi.org/project/elevation/>`_ to obtain an `SRTM 30m Global 1 arc second V003 dataset <https://search.earthdata.nasa.gov/search>`_. Otherwise, use your own dataset.

In this example, we download tiles covering the region of the Central Apennines in Italy into the *data/external* directory.

.. code:: bash

   $ eio clip -o data/Apennines_30m_DEM.tif --bounds 12 41 14 44

Projecting DEM
--------------

Before running *extract-rivers* programme, make sure your DEM is projected into 
a suitable equal areas projection.

.. code:: bash

   $ gdalwarp -t_srs "+proj=lcc +lat_0=52 +lon_0=10 +lat_1=35 +lat_2=65 +ellps=GRS80 +units=m +no_defs" data/Apennines_30m_DEM.tif data/Apennines_30m_DEM_LCC.tif

Running River Extraction
========================

The programme will extract a stream network using a given drainage 
area threshold based on D8 method for single flow direction. 

**Depression Filling method**

While GRASS GIS does not strictly require the DEM to be filled for channel 
extraction (see documentation for further discussion on handling depressions), this
fills the DEM using Richdem's depression filling tool based on Barnes et al. (2016)
priority-flood algorithm.

Parameters
----------

- *Grassdir*: The name of the directory to store all your grass files. In this
   example, I have simply called it grass though have a look at the documentation
   for suggested naming conventions. 

- *DEM*: The projected dem.

- *Shapefile*: A high resolution GSHSS coastline is provided within the directory 
  'data/external'

- *Threshold*: We use a 300 pixel threshold, equivalent to a drainage area of 
  0.27 km\ :sup:`2` for the 30 m DEM. This will determine the drainage density, 
  a higher threshold value will reduce drainage density. 
   
- *No of rivers*: The default is to extract all rivers in the stream network.
  For this example, we will limit the extraction to 50 rivers.
 
Example usage
-------------

.. code:: bash

   $ extract-rivers -p grass -d data/Apennines_30m_DEM_LCC.tif -s data/GSHHS_h_L1.shp -t 300 -n 50

This will take approximately 7 mins to run.

Visualisation
-------------

Before running any visualisations, make sure that your data has been processed to
sort the river data for plotting:

.. code:: bash

   $ process-rivers -i data/raw -o data/interim


River outputs can be visualised by running:

.. code:: bash

   $ visualise-dem
