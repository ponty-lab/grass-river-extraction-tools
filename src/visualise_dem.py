#!/usr/bin/env python

from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import click

def raster_to_grid(gdal_data):

    gdal_band = gdal_data.GetRasterBand(1)
    nodataval = gdal_band.GetNoDataValue()
    data_array = gdal_data.ReadAsArray()

    if np.any(data_array == nodataval):
        data_array[data_array == nodataval] = np.nan

    return np.rot90(data_array, 3)


def hillshade(array, azimuth, angle_altitude):

    # Source: http://geoexamples.blogspot.com.br/2014/03/shaded-relief-images-using-gdal-python.html

    x, y = np.gradient(array)
    slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
    aspect = np.arctan2(-x, y)
    azimuthrad = azimuth*np.pi / 180.
    altituderad = angle_altitude*np.pi / 180.


    shaded = np.sin(altituderad) * np.sin(slope) \
     + np.cos(altituderad) * np.cos(slope) \
     * np.cos(azimuthrad - aspect)
    return 255*(shaded + 1)/2

def plot_dem(grid, directory, name):
    
    print("Plotting DEM")
    
    fig = plt.figure(figsize = (12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.matshow(hillshade(grid, 315, 45), cmap='Greys', alpha=.5, zorder=10)
    cax = ax.imshow(grid, cmap = "viridis")
    plt.title("Topographic Map of %s" % name)
    #Plotting color bar
    im_ratio = grid.shape[0]/grid.shape[1]
    cbar = plt.colorbar(cax, fraction=0.046*im_ratio, pad=0.04)
    cbar.set_label('Elevation, m')
    plt.gca().set_aspect('equal', adjustable='box')
    #Saving figures
    fig.savefig(f"{directory}/dem.png")

def plot_river(x, y1, y2, directory, number):

    print("Plotting River Data")

    fig, ax1 = plt.subplots(1,1,figsize=(12,8), dpi= 80)
    ax1.plot(x, y1, color='tab:blue')

    # Plot Line2 (Right Y Axis)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.plot(x, y2, color='tab:red')

    # Decorations
    # ax1 (left Y axis)
    ax1.set_xlabel('Distance from mouth, km', fontsize=20)
    ax1.tick_params(axis='x', rotation=0, labelsize=12)
    ax1.set_ylabel('Elevation, m', color='tab:blue', fontsize=20)
    ax1.tick_params(axis='y', rotation=0, labelcolor='tab:blue')

    # ax2 (right Y axis)
    ax2.set_ylabel("Drainage area, km$^2$", color='tab:red', fontsize=20)
    ax2.tick_params(axis='y', labelcolor='tab:red')
    ax2.set_title(f"Long Profile for River {number}", fontsize=22)
    fig.savefig(f"{directory}/riv{number}.png")

@click.command()
@click.option('--name', help="Name of region", required=True)
@click.option('--dem', help="Name of lat/lng DEM", required=True)
@click.option('--directory', help="Output directory", required=True)
@click.option('--river', help="River file", required=True)
def visualise(name, dem, directory, river):

    """Simple tool to visualise River Extraction"""

    import csv
    from pathlib import Path

    #Opening raster and plotting dem
    gdal_data = gdal.Open(dem)
    grid = raster_to_grid(gdal_data)
    plot_dem(grid, directory, name)

    #Opening river data and plotting
    x = []
    y1 = []
    y2 = []
    
    r = Path(river)
    number = int(r.name[3:-4])

    with open(river,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        headers = next(plots) 
        for row in plots:
            x.append(float(row[4])/1000)
            y1.append(float(row[3]))
            y2.append(abs(float(row[5]))/1e6)
    plot_river(x, y1, y2, directory, number)

if __name__ == '__main__':
    visualise()