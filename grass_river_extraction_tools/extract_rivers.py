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
#% description: Extracts individual streams from stream network
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


##################
# IMPORT MODULES #
##################

import grass.script as gscript

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
    options, flags = gscript.parser()

    #Parsing arguments
    vectmap = options['stream']
    max_rivers = int(options['max_rivers'])
    print(stream, max_rivers)

    # Connect to vector database for stream network outputted by r.stream.extract
    stream = VectorTopo(vectmap)
    stream.open()
    cur = stream.table.conn.cursor()



    # Index sqlite database
    cur.execute("create index stream_i1 on stream(x2,y2)")
    cur.execute("create index stream_i1 on stream(x2,y2)")

    # Find cat numbers to linking downstream stream segments
    cur.execute("update stream set tostream=(select s2.cat from stream \
                s2 where stream.x2=s2.x1 and stream.y2=s2.y1 and \
                stream.cat<>s2.cat)")

    max_rivers = cur.execute('select COUNT(*) from stream \
                              where stream_type="start"')

    # Open DEM

    DEM = RasterRow('dem')
    DEM.open('r')




if __name__ == "__main__":
    main()


