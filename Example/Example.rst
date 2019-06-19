Example
=======

Quickstart
----------

Testing output from RST file. 
Will it work?

Getting data
-------------

To test this package, we'll need to download a dataset. To do this we can use
`Elevation <https://pypi.org/project/elevation/>`_ to easily download an SRTM dataset. 
Otherwise, use your own merged datasetpdate

Install the latest version of `Elevation <https://pypi.org/project/elevation/>`_ and 
any dependencies not installed:

.. code:: bash

   $ pip install elevation

Download NASA's `SRTM 30m Global 1 arc second V003 <https://search.earthdata.nasa.gov/search>`_ 
for your area of interest. In this example, we are downloading tiles covering the Central Apennines in Italy.

.. code:: bash

   $ eio clip -o Apennines_30m_DEM.tif --bounds 12 41 14 44
