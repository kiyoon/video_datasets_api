#!/bin/bash

if [ $# -lt 2 ]
then
	echo "usage: $0 [frames_dir] [output_dir] "
	echo "Gulp flow dataset that are extracted with Open-MMlab Denseflow."
	exit 1
fi

input_dir="$1"
output_dir="$2"

python ../gulp_jpeg_dir.py "$input_dir" "$output_dir" flow_onefolder --class_folder
