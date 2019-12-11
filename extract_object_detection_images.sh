#!/bin/bash

if [ $# -lt 2 ]
then
	echo "usage: $0 [input_dir] [output_dir]"
	echo "Extracts all tar files in the input_dir, for EPIC-Kitchens object detection images."
	exit 1
fi

input_dir="$1"
output_dir="$2"

tar_files=$(find "$input_dir" -type f -name "*.tar" | sort)

while read line
do
	extract_dir="$output_dir/${line%.tar}"
	mkdir -p "$extract_dir"
	tar xvf "$line" -C "$extract_dir"
done <<< "$tar_files"
