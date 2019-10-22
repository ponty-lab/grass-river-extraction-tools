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
    im_ratio = grid.shape[0]/grid.shape[1]
    cbar = plt.colorbar(cax, fraction=0.046*im_ratio, pad=0.04)
    cbar.set_label('Elevation, m')
    plt.gca().set_aspect('equal', adjustable='box')
    fig.savefig(f"{directory}/dem.png")

def plot_river(x, y, d, z, a, directory, number, river_files, delimiter, name, extent):
    from matplotlib import gridspec
    fig = plt.figure(figsize=(16, 8)) 
    plt.subplots_adjust(wspace=0.9)
    gridspec.GridSpec(3, 2, width_ratios=[1, 1]) 
    ax1 = plt.subplot2grid((4,4), (1,0), colspan=2, rowspan=2)
    ax3 = plt.subplot2grid((4,4), (0,2), colspan=2, rowspan=4)
    ax1.plot(d, z, color='tab:blue')
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.plot(d, a, color='tab:red')
    ax1.set_xlabel('Distance, km', fontsize=12)
    ax1.tick_params(axis='x', rotation=0, labelsize=12)
    ax1.set_ylabel('Elevation, km', color='tab:blue', fontsize=12)
    ax1.tick_params(axis='y', rotation=0, labelcolor='tab:blue')
    ax2.set_ylabel("Area, m$^2$ x 10$^9$ ", color='tab:red', fontsize=12)
    ax2.ticklabel_format(style='sci')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    ax2.set_title(f"{name} River (no. {number})", fontsize=16)
    left, right, bottom, top = extent
    ax3.set_xlim(left, right)
    ax3.set_ylim(bottom, top)
    for river in tqdm(river_files):
        x1, y1 = np.loadtxt(river, usecols=[0,1], delimiter=delimiter, skiprows=1, unpack=True)
        ax3.plot(x1/1000, y1/1000, '-k', lw=0.5)
    
    ax3.plot(x, y, color='tab:blue', lw=3)
    ax3.set_xlabel('x, km')
    ax3.set_ylabel('y, km')

    fig.savefig(f"{directory}/{name}_riv{number}.png")

def plot_riv_num(directory, river_files, font_size, plot_size, delimiter, outfile, extent):
    plt.rcParams.update({'font.size': font_size})
    fig = plt.figure(figsize=plot_size)
    ax = plt.axes()
    #left, right, bottom, top = extent
    #ax.set_xlim(left, right)
    #ax.set_ylim(bottom, top)
    for river in tqdm(river_files):
        print(river)
        _ , fname = os.path.split(river)
        riv_num = re.match("^[^0-9]*([0-9]+)[^0-9]*$", fname).group(1)
        x, y = np.loadtxt(river, usecols=[0,1], delimiter=delimiter, skiprows=1, unpack=True)
        ax.plot(x/1000, y/1000, '-k', lw=0.5)
        ax.text(x[0]/1000, y[0]/1000, riv_num)
    plt.xlabel('x, km')
    plt.ylabel('y, km')
    fig.canvas.draw()
    #plt.tight_layout(pad=2)
    plt.savefig(f"{outfile}", bbox_inches='tight')

@click.group()
def main():
    """
    Plotting tools to visualise river extraction process
    
    """

@main.command('dem')
@click.option('--name', help="Name of region", required=True)
@click.option('--dem', help="Name of lat/lng DEM", required=True)
@click.option('--directory', prompt=True, type=click.Path(exists=True),
                default=os.getcwd(), show_default=True)
def dem (name, dem, directory):
    """
    Plots extent of DEM overlaid on hillshade
    
    """
    click.echo(f"Plotting {dem}")
    gdal_data = gdal.Open(dem)
    grid = raster_to_grid(gdal_data)
    plot_dem(grid, directory, name)

@main.command('river')
@click.option('--directory', type=click.Path(exists=True),
                default=os.getcwd(), show_default=True)
@click.option('--river', help="River file", 
                type=click.Path(exists=True), required=True)
@click.option('--river-dir', help="River directory", 
                type=click.Path(exists=True), required=True)
@click.option('--delimiter', default=' ', show_default=True)
@click.option('--name')
@click.option('--extent', help="change map extent", 
                type=(int, int, int, int), 
                default=(None, None, None, None))
def river (directory, river, river_dir, delimiter, name, extent):
    """
    Plotting individual river profiles
    
    """
    _ , fname = os.path.split(river)
    print(f"Plotting river profile for river: <{fname}>")
    riv_num = re.match("^[^0-9]*([0-9]+)[^0-9]*$", fname).group(1)
    river_files = glob.glob(os.path.join(river_dir, '*riv*'))
    x, y, z, d, a = np.loadtxt(river, usecols=[0, 1, -3, -2, -1], 
                                delimiter=delimiter, skiprows=1, unpack=True)
    plot_river(x/1000, y/1000, d/1000, z/1000, np.abs(a/1e9), 
                directory, riv_num, river_files, 
                delimiter, name, extent)

@main.command('map_rivnum')
@click.option('-d', '--directory', type=click.Path(exists=True),
                default=os.getcwd(), show_default=True)
@click.option('-r', '--river-dir', help="River directory", 
                type=click.Path(exists=True), required=True)
@click.option('-f', '--font-size', help="change font size of labels", 
                default=10, show_default=True)
@click.option('-p', '--plot-size', help="change plot size", type=(int, int),
                nargs=2, default=[60, 60], show_default=True)
@click.option('-o', '--outfile', default='river_numbers.png', show_default=True)
@click.option('--delimiter', default=' ', show_default=True)
@click.option('--extent', help="change map extent", 
                type=(int, int, int, int), 
                default=(None, None, None, None))
def map (directory, river_dir, font_size, plot_size, delimiter, outfile, extent):
    """
    Plotting map of river numbers

    """
    print(f"Plotting map of river numbers using directory: <{river_dir}>")
    rivers = glob.glob(os.path.join(river_dir, '*riv*'))
    plot_riv_num(directory, rivers, font_size, list(plot_size), 
                    delimiter, outfile, extent)

if __name__ == '__main__':
    main()