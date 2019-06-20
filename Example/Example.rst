Quickstart
===========

.. image:: https://github.com/pontc/grass-river-extraction-tools/blob/master/Example/figures/dem.png

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
extraction (see `documentation <https://grass-gis-to-extract-river-profiles.readthedocs.io/en/latest/>`_ 
for further discussion on handling depressions), DEM's are filled using Richdem's 
depression filling tool based on Barnes et al. (2016) priority-flood algorithm.

Parameters
----------

- *Grassdir*: The name of the directory to store all your grass files. In this
   example, I have simply called it grass though have a look at the `documentation <https://grass-gis-to-extract-river-profiles.readthedocs.io/en/latest/>`_ 
   for suggested naming conventions.

- *DEM*: The projected dem.

- *Shapefile*: A high resolution GSHSS coastline is provided within the directory 
  *./data*

- *Threshold*: We use a 300 pixel threshold, equivalent to a drainage area of 
  0.27 km\ :sup:`2` for the 30 m DEM. This will determine the drainage density, 
  a higher threshold value will reduce stream network density. 
   
- *No of rivers*: The default is to extract all rivers in the stream network.
  For this example, we will limit the extraction to 50 rivers.
 
Example usage
-------------

.. code:: bash

   $ extract-rivers -p grass -d data/Apennines_30m_DEM_LCC.tif -s data/GSHHS_h_L1.shp -t 300 -n 50

This will take approximately 7 mins to run.

Extract from river ascii output files:

::

   east,north,cat,elevation_m,distance_m,drainage_area_m2
   287177.44940819,-1014567.43537917,4,1372.00000000,27.92307279,279911.57985879
   287149.52633541,-1014539.51230638,5,1368.00000000,67.41226103,285369.46581704
   287177.44940819,-1014511.58923359,6,1368.00000000,106.90144927,287708.55979915
   287177.44940819,-1014483.6661608,7,1359.00000000,134.82452206,288488.25779319
   287177.44940819,-1014455.74308801,8,1352.00000000,162.74759485,356321.98327429
   287177.44940819,-1014427.82001522,9,1342.00000000,190.67066764,368017.45318482
   287149.52633541,-1014399.89694243,10,1335.00000000,230.15985588,372695.64114904
   287121.60326262,-1014371.97386965,11,1331.00000000,269.64904412,391408.39300589
   287093.68018983,-1014371.97386965,12,1328.00000000,297.57211691,772680.71208932
   287065.75711704,-1014371.97386965,13,1323.00000000,325.49518970,854549.00146306
   287037.83404425,-1014344.05079686,14,1315.00000000,364.98437794,873261.75331992
   287009.91097146,-1014344.05079686,15,1313.00000000,392.90745072,890415.10918870
   286981.98789867,-1014371.97386965,16,1313.00000000,432.39663897,895093.29715291
   286954.06482589,-1014371.97386965,17,1311.00000000,460.31971175,902110.57909923
   286926.1417531,-1014371.97386965,18,1307.00000000,488.24278454,902890.27709327
   286898.21868031,-1014371.97386965,19,1304.00000000,516.16585733,909907.55903959
   286870.29560752,-1014399.89694243,20,1300.00000000,555.65504557,958248.83466980
   286842.37253473,-1014371.97386965,21,1292.00000000,595.14423381,959808.23065787
   286814.44946194,-1014344.05079686,22,1281.00000000,634.63342205,973842.79455051
   286786.52638915,-1014316.12772407,23,1280.00000000,674.12261030,976961.58652666
   286758.60331637,-1014316.12772407,24,1278.00000000,702.04568308,981639.77449087
   286730.68024358,-1014288.20465128,25,1270.00000000,741.53487132,983199.17047894


Visualisation
-------------

.. image:: https://github.com/pontc/grass-river-extraction-tools/blob/master/Example/figures/riv2858.png
   :scale: 60 %

Your rivers are ready for plotting and analysis! River outputs can be visualised by running:

.. code:: bash

   $ visualise-dem --name "Central Apennines" --dem data/Apennines_30m_DEM.tif --directory figures/ --river data/raw/riv2858.dat
