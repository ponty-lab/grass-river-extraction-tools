#!/bin/bash

# ---------------------------------------------------------------
#      This script extracts river profiles using GRASS GIS tools 
#      for use with the 2d river inversion model
#
#      Carla Pont - 17/June/2019
# ---------------------------------------------------------------


##### Functions

usage() {
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
   echo "        -n | --number           max number of rivers to extract"
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
      -n | --number )
         shift
         NO_RIVERS=$1
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

if [[ -z $GRASSDIR || -z $DEM || -z $COAST || -z $THRESHOLD || -z $NO_RIVERS ]]; then
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

#Linking river segments to their downstream portion using 
#its unique cat number

v.db.addcolumn stream_300 columns="x1 double,x2 double,y1 double,y2 double,tostream int"
v.to.db map=stream_300 option=start columns=x1,y1
v.to.db map=stream_300 option=end columns=x2,y2

db.execute sql="create index stream_300_i1 on stream_300(x2,y2)"
db.execute sql="create index stream_300_i2 on stream_300(x1,y1)"

db.execute sql="update stream_300 set tostream=(select s2.cat from stream_300 s2 where stream_300.x2=s2.x1 and stream_300.y2=s2.y1)"

#Looping through channel heads to extract rivers

eval `g.region -g`
SQ_M=$( echo "${ewres}*${nsres}" | bc -l )
res=$( echo "${nsres}" )
echo ""
echo ""
echo "Using resolution: $res and cell area: $SQ_M m^2"

#Checking number of rivers doesn't exceed number of start_node records

max_rivnum=`db.select -c sql='select COUNT(*) from stream_300 where stream_type="start"'`

if [ "$NO_RIVERS" -lt "${max_rivnum}" ]
   then
      lim="$NO_RIVERS"
   else
      lim="${max_rivnum}"
fi

#Loop to extract river profiles. 
#Output ascii file contains six columns: 
#X, Y, cat, length, elev, drainage area (m**2)

time for start_node in `db.select -c sql='select cat from stream_300 where stream_type="start" order by random() limit '${lim}''`; do 
	echo "$start_node"
   i=$(( ${i} + 1))
   #Extract linking stream segments
   v.extract -d input=stream_300 output=line_${i} where="cat in (with recursive cats(cat) as (values(${start_node}) union all select tostream from stream_300 s, cats where s.cat=cats.cat) select cat from cats where cat is not null)" new=0 $command_args
   #Convert to polyline (to remove duplicate vertices)
   v.build.polylines input=line_${i} output=cpath_${i} $command_args
   #Extract X, Y coordinates and distance along channel
   v.to.points -i input=cpath_${i} output=pnt_${i} use=vertex dmax=${nsres} layer=-1 $command_args
   #Remove superfluous points for v.build.polylines
   v.extract input=pnt_${i} where="along > 0" output=cpathpnt_${i} layer=2 $command_args
   #Extract elevation at each point
   v.what.rast cpathpnt_$i raster=dem column=elev layer=2 $command_args
   #Extract flow accumulation at each point
   v.what.rast cpathpnt_$i raster=facc column=accum_pixels layer=2 $command_args
   v.db.addcolumn cpathpnt_$i columns="accum_area double" layer=2 $command_args
   #Convert flow accumulation pixels to m^2
   v.db.update cpathpnt_$i column=accum_area query_col="accum_pixels*${SQ_M}" layer=2 $command_args
   #Drop column with flow accumulation pixels
   v.db.dropcolumn cpathpnt_$i columns="accum_pixels" layer=2 $command_args
   #Output each stream channel in a separate ascii file
   v.out.ascii -c input=cpathpnt_$i layer=2 columns=* separator=' ' output=riv$i.dat $command_args
   echo ""
   echo "----------------------------"
   echo " River $i of ${lim} created "
   echo "----------------------------"
   echo ""
done

echo "River Extraction Complete!"