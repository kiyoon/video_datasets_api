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
	input_to_output=$(echo "$line" | sed "s|$input_dir|$output_dir|")
	extract_dir="${input_to_output%.tar}"
	mkdir -p "$extract_dir"
	echo "Extracting to $extract_dir"
	tar xf "$line" -C "$extract_dir"
done <<< "$tar_files"
