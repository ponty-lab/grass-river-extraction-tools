#!/usr/bin/env python

from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import click
import os
import glob
from tqdm import tqdm
import re

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

def plot_river(x, y, d, z, a, directory, number, river_files):
    from matplotlib import gridspec
    fig = plt.figure(figsize=(16, 8)) 
    plt.subplots_adjust(wspace=0.9)
    gridspec.GridSpec(3, 2, width_ratios=[1, 1]) 
    ax1 = plt.subplot2grid((4,4), (1,0), colspan=2, rowspan=2)
    ax3 = plt.subplot2grid((4,4), (0,2), colspan=2, rowspan=4)
    ax1.plot(d, z, color='tab:blue')
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.plot(d, a, color='tab:red')
    ax1.set_xlabel('Distance from headwaters, km', fontsize=12)
    ax1.tick_params(axis='x', rotation=0, labelsize=12)
    ax1.set_ylabel('Elevation, m', color='tab:blue', fontsize=12)
    ax1.tick_params(axis='y', rotation=0, labelcolor='tab:blue')
    ax2.set_ylabel("Drainage area, km$^2$", color='tab:red', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='tab:red')
    ax2.set_title(f"Long Profile for River {number}", fontsize=16)

    for river in tqdm(river_files):
        x1, y1 = np.loadtxt(river, usecols=[0,1], unpack=True)
        ax3.plot(x1/1000, y1/1000, '-k', lw=0.5)
    ax3.plot(x, y, color='tab:blue', lw=3)
    ax3.set_xlabel('x, km')
    ax3.set_ylabel('y, km')

    fig.savefig(f"{directory}/riv{number}.png")

def plot_riv_num(directory, river_files, font_size, plot_size):
    plt.rcParams.update({'font.size': font_size})
    fig = plt.figure(figsize=plot_size)
    ax = plt.axes()
    for river in tqdm(river_files):
        _ , fname = os.path.split(river)
        riv_num = re.match("^[^0-9]*([0-9]+)$", fname).group(1)
        x, y = np.loadtxt(river, usecols=[0,1], unpack=True)
        ax.plot(x/1000, y/1000, '-k', lw=0.5)
        ax.text(x[0]/1000, y[0]/1000, riv_num)
    plt.xlabel('x, km')
    plt.ylabel('y, km')
    plt.tight_layout(pad=2)
    plt.savefig(f"{directory}/river_numbers.png", bbox_inches='tight')

@click.group()
def main():
    """Plotting tools to visualise river extraction process"""

@main.command('dem')
@click.option('--name', help="Name of region", required=True)
@click.option('--dem', help="Name of lat/lng DEM", required=True)
@click.option('--directory', prompt=True, type=click.Path(exists=True),
                default=os.getcwd(), show_default=True)
def dem (name, dem, directory):
    """Plots extent of DEM overlaid on hillshade"""

    click.echo(f"Plotting {dem}")
    gdal_data = gdal.Open(dem)
    grid = raster_to_grid(gdal_data)
    plot_dem(grid, directory, name)

@main.command('river')
@click.option('--directory', type=click.Path(exists=True),
                default=os.getcwd(), show_default=True)
@click.option('--river', help="River file", type=click.Path(exists=True), required=True)
@click.option('--river-dir', help="River directory", type=click.Path(exists=True),
                required=True)
def river (directory, river, river_dir):
    """Plotting individual river profiles"""
    _ , fname = os.path.split(river)
    print(fname)
    riv_num = re.match("^[^0-9]*([0-9]+)$", fname).group(1)
    river_files = glob.glob(os.path.join(river_dir, 'obs_riv*'))
    x, y, z, d, a = np.loadtxt(river, usecols=[0, 1, -3, -2, -1], unpack=True)
    plot_river(x/1000, y/1000, d/1000, z, a/1e6, directory, riv_num, river_files)

@main.command('map_rivnum')
@click.option('--directory', type=click.Path(exists=True),
                default=os.getcwd(), show_default=True)
@click.option('--river-dir', help="River directory", type=click.Path(exists=True),
                required=True)
@click.option('--font-size', help="change font size of labels", default=10,
                show_default=True)
@click.option('--plot-size', help="change plot size", type=(int, int),
                nargs=2, default=[60, 60], show_default=True)
def map (directory, river_dir, font_size, plot_size):
    """Plotting map of river numbers"""
    rivers = glob.glob(os.path.join(river_dir, 'obs_riv*'))
    plot_riv_num(directory, rivers, font_size, list(plot_size))

if __name__ == '__main__':
    main()