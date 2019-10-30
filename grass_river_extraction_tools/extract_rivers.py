#!/usr/bin/env python

########################################
#
#MODULE:        Update to v.stream.network
#
# PURPOSE:      This modules extracts individual streams from the stream 
#               network with characteristics of length, elevation and 
#               drainage area
#
# COPYRIGHT:    (c) 2019 Carla Pont and Will Slater
#
#               This program is free software under the GNU General Public
#               License (>=v2). Read the file COPYING that comes with GRASS
#               for details.
#
# REQUIREMENTS:
#      -  uses inputs from r.stream.extract
#
#############################################################################


#%module
#% description: Extracts individual streams from a stream network
#% keyword: vector
#% keyword: stream network
#% keyword: hydrology
#% keyword: geomorphology
#%end

#%option G_OPT_V_INPUT
#% key: stream
#%end

#%option
#%  key: max_rivers
#%  key_desc: value
#%  type: integer
#%  description: Maximum number of rivers to extract. By default all of them (-1)
#%  answer: -1
#%  required: no
#%end

"""Insert:
elevation map
accumulation map
units
output - vector map or text file"""

##################
# IMPORT MODULES #
##################

import grass.script as gscript
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules.shortcuts import vector as v
from grass.pygrass.vector import Vector, VectorTopo
from grass.pygrass.raster import RasterRow
from grass.pygrass import vector
import numpy as numpy
import matplotlib.pyplot as plt
import sqlite3

###############
# MAIN MODULE #
###############

class CursorByName():
    def __init__(self, cursor):
        self._cursor = cursor
    
    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()

        return { description[0]: row[col] for col, description in enumerate(self._cursor.description) }

def main():
    """
    Links entire stream network to its downstream network to extract indvidual rivers
    """

    options, flags = gscript.parser()

    #Parsing arguments
    stream = options['stream']
    max_rivers = int(options['max_rivers'])
    print(stream, max_rivers)

    # Connect to vector database for stream network outputted by r.stream.extract
    stream = VectorTopo(stream)
    stream.open()
    cur = stream.table.conn.cursor()

    # Create new columns in sqlite database to hold downstream cat numbers

    v.db.addcolumn()

    # Index sqlite database
    cur.execute("create index stream_i1 on stream(x2,y2)")
    cur.execute("create index stream_i1 on stream(x2,y2)")

    # Find cat numbers to linking downstream stream segments
    cur.execute("update stream set tostream=(select s2.cat from stream \
                s2 where stream.x2=s2.x1 and stream.y2=s2.y1 and \
                stream.cat<>s2.cat)")

    total_rivers = cur.execute('select COUNT(*) from stream \
                              where stream_type="start"')
    
    # Extract rivers of interest
    # Checking whether rivers to extract exceeds maximum number of rivers to extract

    if total_rivers < max_rivers:
        max_rivers = total_rivers
    else:
        max_rivers = max_rivers

    # Open DEM

    region = gs.region()
    area = float(cells) * g.script.region()['ewres'] * g.script.region()['nsres']
    print(f"Using resolution {region} and cell area {area} m^2")

    DEM = RasterRow('dem')
    DEM.open('r')

    geometry.Line
    stream.cat
    columns = [ ('cat', 'INTEGER'),
                ('elevation_m', 'DOUBLE PRECISION'),
                ('distance', 'DOUBLE PRECISION'),
                ('area_m2', 'DOUBLE PRECISION'),
                ]

    #Loop through rivers of interest

    for start_cat in cur.execute( f'SELECT cat 
                                    FROM stream 
                                    WHERE stream_type="start" 
                                    ORDER BY random() 
                                    LIMIT {max_rivers}'):

        selected_cats = cur.execute('select cat from stream where cat in (with recursive cats(cat) as (values({start_node}) union all select tostream from stream s, cats where s.cat=cats.cat) select cat from cats where cat is not null)')

        points = []
        for cat in selected_cats:
            for line in stream.cat(cat, 'lines'):
                points.extend(line.to_list())


        # Extract linking downstream sections

        v.extract( input=vectmap, output=f"linkedsegments_{start_cat}", where=f'cat in (with recursive cats(cat) as (values({start_node}) union all select tostream from stream s, cats where s.cat=cats.cat) select cat from cats where cat is not null)', new=0, overwrite=gscript.overwrite() )

        # Convert to polyline to remove duplicate vertices

        v.build.polylines( input=f"linkedsegments_{startcat}", output=f"river_{start_cat}", overwrite=gscript.overwrite() )

        # Extract coordinates as numpy array

        coords = []
                for k, coordinates in enumerate(stream, start=1):
                    stream_k = stream.read(k)
                    if type(stream_k).cat is vector.geometry.Line:
                        if stream_k.cat in selected_cats:
                            coords.append(stream_k.to_array())



if __name__ == "__main__":
    main()


