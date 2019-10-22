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
from grass.pygrass.vector import VectorTopo

###############
# MAIN MODULE #
###############

def main():
    options, flags = gscript.parser()
    stream = options['stream']
    max_rivers = int(options['max_rivers'])
    print(stream, max_rivers)

    #Linking river segments to their downstream portion using its unique cat number
    columns =  [('x1 DOUBLE PRECISION'),
                ('y1 DOUBLE PRECISION'),
                ('x2 DOUBLE PRECISION'),
                ('y2 DOUBLE PRECISION'),
                ('tostream INTEGER')]
    
    #with VectorTopo(stream, mode='rw') as stream:



    gscript.run_command('v.db.addcolumn', map=stream, columns=columns)
    gscript.run_command('v.to.db', map=stream, option='start', columns=['x1','y1'])
    gscript.run_command('v.to.db', map=stream, option='end', columns=['x2','y2'])

    sql_instructions =  ["""
                        CREATE index stream_i1 on stream(x2,y2);
                        CREATE index stream_i2 on stream(x1,y1);
                        UPDATE stream SET tostream=(select s2.cat from stream s2 where stream.x2=s2.x1 and stream.y2=s2.y1 and stream.cat<>s2.cat);
                        """]

    gscript.run_command('db.execute', sql="CREATE index stream_i1 on stream(x2,y2)")
    gscript.run_command('db.execute', sql="CREATE index stream_i2 on stream(x1,y1)")
    gscript.run_command('db.execute', sql="UPDATE stream SET tostream=(select s2.cat from stream s2 where stream.x2=s2.x1 and stream.y2=s2.y1 and stream.cat<>s2.cat)")

    area = float(cells) * gscript.region()['nsres'] * gscript.region()['ewres']


if __name__ == "__main__":
    main()
