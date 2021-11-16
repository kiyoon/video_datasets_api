#!/bin/bash

if [ $# -lt 2 ]
then
	echo "usage: $0 [input_dir] [output_dir] [num_videos = 20]"
	echo "chooses 20 video files randomly from the input directory and run Faster R-CNN"
	exit 1
fi

input_dir="$1"
output_dir="$2"
if [ $# -lt 2 ]
then
	num_videos=20
else
	num_videos="$3"
fi

files=$(find "$input_dir" -type f -name "*.avi" -o -name "*.mp4" | shuf | head -${num_videos})

input_dir_parent=$(dirname "$input_dir")

while read line
do
	input_file="$line"
	output_file=$(echo "$input_file" | sed "s|$input_dir_parent|$output_dir|")

	echo "Processing $input_file"
	echo "Saving to $output_file"

	mkdir -p $(dirname "$output_file")
	./object_detector.py --video-input "$input_file" --confidence-threshold 0.5 --output "$output_file"
done <<< "$files"

