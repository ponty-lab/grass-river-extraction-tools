#!/usr/bin/env python

import time
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import csv

#riv_list=['riv11350.dat']

riv_list=['riv11350.dat', 'riv23354.dat', 'riv30977.dat', 
    'riv47648.dat', 'riv6056.dat', 'riv11847.dat', 'riv24591.dat',
    'riv31.dat', 'riv4887.dat', 'riv62637.dat', 'riv14105.dat',
    'riv24982.dat', 'riv32962.dat', 'riv50225.dat', 'riv64388.dat', 
    'riv1548.dat']

def xy(river):
    x = []
    y = []
    y1 = []
    with open(river,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        headers = next(plots) 
        for row in plots:
            #li = (float(row[4])/1000, float(row[3]))
            #li2 = (float(row[4])/1000, abs(float(row[5]))/1e6)
            #xy.append(li)
            #xy1.append(li2)
            x.append(float(row[4])/1000)
            y.append(float(row[3]))
            y1.append(abs(float(row[5]))/1e6)
    return x, y, y1

def plot_river(plot1, plot2):

    print("Plotting River Data")

    #fig, ax1 = plt.subplots(1,1,figsize=(12,8), dpi= 80)
    ax.plot(plot1, color='tab:blue')

    # Plot Line2 (Right Y Axis)
    ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.plot(plot2, color='tab:red')

    # Decorations
    # ax1 (left Y axis)
    ax.set_xlabel('Distance from mouth, km', fontsize=20)
    ax.tick_params(axis='x', rotation=0, labelsize=12)
    ax.set_ylabel('Elevation, m', color='tab:blue', fontsize=20)
    ax.tick_params(axis='y', rotation=0, labelcolor='tab:blue')

    # ax2 (right Y axis)
    ax2.set_ylabel("Drainage area, km$^2$", color='tab:red', fontsize=20)
    ax2.tick_params(axis='y', labelcolor='tab:red')
    #ax2.set_title(f"Long Profile for River {number}", fontsize=22)

    return fig
    #fig.savefig(f"{directory}/riv{number}.png")

def loop_plot(plots):
    figs={}
    axs={}
    for idx,plot in enumerate(plots):
        figs[idx]=plt.figure()
        axs[idx]=figs[idx].add_subplot(111)
        axs[idx].plot(plot[0],plot[1])
    return figs, axs

def plot_multiples (plot, plot1):

    num=0
    for column in df.drop('x', axis=1):
    num+=1
 
    # Find the right spot on the plot
    plt.subplot(3,3, num)
 
    # Plot the lineplot
    plt.plot(df['x'], df[column], marker='', color=palette(num), linewidth=1.9, alpha=0.9, label=column)
 
    # Same limits for everybody!
    plt.xlim(0,10)
    plt.ylim(-2,22)
 
    # Not ticks everywhere
    if num in range(7) :
        plt.tick_params(labelbottom='off')
    if num not in [1,4,7] :
        plt.tick_params(labelleft='off')
 
    # Add title
    plt.title(column, loc='left', fontsize=12, fontweight=0, color=palette(num) )


    fig, ax = plt.subplots(4, 4, sharex='col', sharey='row')
    for i in range(4):
        for j in range(4):
            ax[i,j].plot(plot[0],plot[1], color='tab:blue')
            ax2 = ax.twinx()
            ax2[i,j].plot(plot1[0],plot1[1], color='tab:red')
    return fig, ax

    #plot_list = [axa[i].plot(xy_list[i]), for i in range(len(xy_list))]
    #xy2_list = ax2.plot(x, y2, color='tab:red')
    #fig.tight_layout()
    #title = int(riv_list[i][3:-4])

#xy_list = xy(riv_list[i], for i in range(len(riv_list)))
coord_x = []
coord_y = []
coord_y1 = []
for n in riv_list:
    x, y, y1 = xy(n)
    coord_x.append(x)
    coord_y.append(y)
    coord_y1.append(y1)
plot = zip(coord_x, coord_y)
plot1 = zip(coord_x, coord_y1)
#figs, axs = loop_plot(plots)
fig = plot_multiples(plot, plot1)
plt.show()
fig.savefig("../../figures/multiple_plots.png")
