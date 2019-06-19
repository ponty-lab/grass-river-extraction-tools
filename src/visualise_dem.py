#!/usr/bin/env python

from osgeo import gdal
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
import click

@click.command()
@click.option('--dem', help="Name of DEM", required=True)
@click.option('--region', help="Name of region", required=True)

def plot(dem, region):
    """Simple program to plot DEM"""

    gdal_data = gdal.Open(dem)
    gdal_band = gdal_data.GetRasterBand(1)
    nodataval = gdal_band.GetNoDataValue()

    # convert to a numpy array
    data_array = gdal_data.ReadAsArray().astype(np.float)

    # replace missing values if necessary
    if np.any(data_array == nodataval):
        data_array[data_array == nodataval] = np.nan

    y, x = np.where(data_array != nodataval)
    topo = data_array[0:max(x)+1, 0:max(y)+1]

    #Plot out data with Matplotlib's 'figure'
    fig = plt.figure(figsize = (12, 8))
    ax = fig.add_subplot(111)
    plt.imshow(topo, cmap = "viridis")
    plt.title("Elevation DEM of %s" % region)
    cbar = plt.colorbar()
    cbar.set_label('meters')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

if __name__ == '__main__':
    plot()