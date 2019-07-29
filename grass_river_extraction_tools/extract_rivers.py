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

###############
# MAIN MODULE #
###############

def main():
    options, flags = gscript.parser()
    stream = options['stream']
    max_rivers = int(options['max_rivers'])
    print(stream, max_rivers)

if __name__ == "__main__":
    main()


