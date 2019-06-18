#!/bin/bash

usage()
{
   echo ""
   echo "Simple script to mosaic and project SRTM grids for use in GRASS"
   echo "" 
   echo "Usage:"
   echo "   -d | --dir           Download folder containing zipped SRTM granules"
   echo "   -o | --out-dir       Output directory for unzipped SRTM granules"
   echo "   -f | --dem           Name of new mosaiced Raster"
   echo "   -p | --projection    Projection using PROJ.4 cs2cs string format"
   echo ""  
   exit 1
}


#Set default parameters

#output_dir=$HOME/italy/dem
#input_path=$HOME/Downloads/*.hgt.zip
#proj='EPSG:3034'
#name='italy'

#Check inputs and parse them

while [ "$1" != "" ]; do
   case $1 in
      -d | --dir )
         shift
         input_path="{$1%/}/*.hgt.zip"
         ;;
      -o | --outdir )
         shift
         output_dir=$1
         ;;
      -f | --dem )
         shift
         name=$1
         ;;
      -p | --projection )
         shift
         proj=$1
         ;;
      -h | --help )
         usage
         exit
         ;;
      * )
         echo "Some or all of parameters not recognised"
         helpFunction
         exit 1
   esac
   shift
done

if [[ -z $input_path || -z $name || -z $proj ]]; then
	echo "Error: required arguments not set"
	usage
	exit 1
fi

#Unzip files into destination folder

mkdir -p $output_dir
echo ""
echo "Directory: $output_dir created"

files=`ls ${input_path}`

for f in $files; do
    unzip $f -d ${output_dir}
done

echo "--------------------------------------------------------------"
echo "Raw dem tiles unzipped to $output_dir"
echo "--------------------------------------------------------------"

#Mosaicing and reprojecting grid into New Raster

cd $output_dir

ls **/*.bil >> DEMs.txt

if [[ -f $name.tif ]]; then
   echo "$name.tif already exists"
   echo "Delete dem file and run script again OR supply another name using -f flag"
   
else
   echo "Mosaicing SRTM tiles to new raster"
   echo""
   gdal_merge.py -of Gtiff -n -32768 -a_nodata -32768 -o merged_dem.tif --optfile DEMs.txt
   echo "--------------------------------------------------------------"
   
   echo "Reprojecting new raster $name.tif"
   echo ""
   gdalwarp -t_srs "$proj" merged_dem.tif $name.tif
   echo "--------------------------------------------------------------"
fi

#Cleaning up directory
#rm -f merged_dem.tif DEMs.txt 

echo "--------------------------------------------------------------"
echo "done"
echo "--------------------------------------------------------------"