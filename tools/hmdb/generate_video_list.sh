#!/bin/bash

if [ $# -lt 1 ]
then
	echo "usage: $0 [videos_dir]"
	echo "Find videos, sort and save the list to a file hmdb_videos_list.txt."
	echo "It will ignore the .avi extension."
	exit 1
fi

input_dir="$1"

all_videos=$(find "$input_dir" -mindepth 2 -maxdepth 2 -name "*.avi" -type f | sort)
relative_path=$(echo "$all_videos" | xargs -I{} realpath --relative-to="$input_dir" {} | sed 's/.avi$//')
echo "$relative_path" > hmdb_videos_list.txt
