#!/bin/bash

# ---------------------------------------------------------------
#      This script extracts river profiles using GRASS GIS tools 
#      for use with the 2d river inversion model
#
#      Carla Pont - 15/June/2019
# ---------------------------------------------------------------


##### Functions

usage()
{
   echo ""
   echo "An automated method to extract rivers using GRASS GIS"
   echo "" 
   echo "Usage: $0 [OPTIONS] -d <grassdir> -f <dem> -s <shapefile> -t <threshold>"
   echo ""
   echo "ARGUMENTS"
   echo "	-d | --grassdir		GRASS PROJECT directory"
   echo "	-f | --dem		Filled DEM to upload"
   echo "	-s | --shapefile	Shapefile to mask DEM"
   echo "	-t | --threshold	minimum catchment size (pixels)"
   echo "OPTIONS"
   echo "	-o | --overwrite	Overwrite existing files"
   echo "	-h | --help		help"
   echo ""  
   exit 1
}

##### Main

# Read input parameters from command line

args=$*

while [ "$1" != "" ]; do
   case $1 in
      -d | --grassdir )
         shift
         GRASSDIR=$1
         ;;
      -f | --dem )
         shift
         DEM=$1
         ;;
      -s | --shapefile )
         shift
         COAST=$1
         ;;
      -t | --threshold )
         shift
         THRESHOLD=$1
         ;;
	  -o | --overwrite )
	  	 shift
		 command_args='--overwrite'
		 ;;
      -h | --help )
         usage
         exit
         ;;
      * )
         echo "Error: $1 not recognised"
         usage
         exit 1
   esac
   shift
done

#Check if all command line arguments are present

if [[ -z $GRASSDIR || -z $DEM || -z $COAST || -z $THRESHOLD ]]; then
	echo "Error: required arguments not set"
	usage
	exit 1
fi

# Checks if you are in GRASS GIS environment, 
# else starts the environment to run the script

#[POSSIBLE TO INCLUDE OPTION TO USE TMP LOCATION?]

if [[ -z $GISBASE ]]; then
	grass77 -e -c ${DEM} ${GRASSDIR}
   echo ""
   echo "------------------------------------"
	echo "Starting GRASS GIS with ${0} ${args}"
   echo "------------------------------------"
   echo ""
	grass77 --text ${GRASSDIR}/PERMANENT --exec ${0} ${args}
	exit
fi

#Loading projected and filled DEM into GRASS

r.in.gdal input=$DEM output=dem $command_args

#Set region to DEM

echo ""
echo "----------------------------"
echo "Computational region set to:"
echo "----------------------------"
g.region raster=dem -p

#Mask DEM using a high resolution coastline data
r.mask -r
v.import input=$COAST output=coast extent=region $command_args
r.mask vector=coast
echo ""
echo "-----------------------"
echo "DEM masked to coastline"
echo "-----------------------"
echo ""

#Calculate flow accumulation using a SFD
echo "----------------------------------------------------------"
echo "Extracting flow accumulation using a single flow direction"
echo "----------------------------------------------------------"
echo ""
r.watershed -s -m ele=dem acc=facc memory=10000 $command_args

#Calculate stream network
echo ""
echo "------------------------------------------------------------"
echo "Extracting stream network using THRESHOLD: $THRESHOLD pixels"
echo "------------------------------------------------------------"
echo ""

r.stream.extract elevation=dem accumulation=facc threshold=$THRESHOLD stream_rast=stream_$THRESHOLD stream_vector=stream_$THRESHOLD direction=fdir $command_args

#Randomly extract points from the DEM using minimum flow accumulation to use as starting points for channel initiation

echo "Extracting random points for stream extraction using THRESHOLD: $THRESHOLD"
r.mapcalc "facc_$THRESHOLD = if( 'facc' == $THRESHOLD, 1, null())" $command_args
echo "Exporting X Y coordinates to file: coords.dat"
r.to.vect input=facc_$THRESHOLD output=facc_$THRESHOLD type=point $command_args
v.out.ascii in=facc_$THRESHOLD out=coords.dat format=point layer=-1 separator=',' $command_args

#v.out.ascii in=stream_$THRESHOLD where="stream_type=start" out=coords.dat format=point layer=-1 separator=',' --o

#Determining cell resolution to calculate drainage area (m^2)

eval `g.region -g`
SQ_M=$( echo "${ewres}*${nsres}" | bc -l )
res=$( echo "${nsres}" )
echo ""
echo ""
echo "Using resolution: $res and cell area: $SQ_M m^2"

#Converting flow direction to degrees

echo ""
echo "--------------------------------------------"
echo "Converting flow direction raster to degrees "
echo "--------------------------------------------"
echo ""
r.mapcalc "fdir_deg = if(fdir != 0, 45. * abs(fdir), null())"

#Loop to extract river profiles. 
#Output ascii file contains five columns: 
#X, Y, cat, length, elev, drainage area (m**2)

i=0
while read X Y ; do
   total=`cat coords.dat | wc -l`
	echo "$X, $Y"
	i=$(( ${i} + 1))
   #Determine individual stream path
	r.drain input=dem direction=fdir_deg output=cpath_$i drain=cpath_$i start_coordinates=$X,$Y --o 
   #Extract X, Y coordinates and distance along channel
	v.to.points input=cpath_$i output=cpathpnt_$i use=vertex dmax=$res layer=-1 --o
   #Extract elevation at each point
	v.what.rast cpathpnt_$i raster=dem column=elev layer=2 --o
   #Extract flow accumulation at each point
	v.what.rast cpathpnt_$i raster=facc column=accum_pixels layer=2 --o
	v.db.addcolumn cpathpnt_$i columns="accum_area double" layer=2 --o
   #Convert flow accumulation pixels to m^2
	v.db.update cpathpnt_$i column=accum_area query_col="accum_pixels*${SQ_M}" layer=2 --o
   #Drop column with flow accumulation pixels
	v.db.dropcolumn cpathpnt_$i columns="accum_pixels" layer=2 --o
   #Output each stream channel in a separate ascii file
	v.out.ascii -c input=cpathpnt_$i layer=2 columns=* separator=' ' output=riv$i.dat --o
   echo ""
   echo "----------------------------"
	echo " River $i of $total created "
   echo "----------------------------"
   echo ""
done < coords.dat

echo "River Extraction Complete!"
