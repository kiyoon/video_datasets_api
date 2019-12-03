#!/bin/bash

if [ $# -lt 3 ]
then
	echo "usage: $0 [input_dir (either train or test)] [output_dir] [action_labels.csv]"
	exit 1
fi

input_dir="$1"
output_dir="$2"
action_labels_csv="$3"

action_labels=$(cat "$action_labels_csv")

mkdir -p "$output_dir"

while read line
do
	id=$(echo "$line" | awk -F , '{print $1}')
	participant=$(echo "$line" | awk -F , '{print $2}')
	video=$(echo "$line" | awk -F , '{print $3}').MP4
	start_time=$(echo "$line" | awk -F , '{print $5}')
	end_time=$(echo "$line" | awk -F , '{print $6}')
	verb=$(echo "$line" | awk -F , '{print $9}')

	ffmpeg -i "$input_dir/$participant/$video" -vf scale=320:240:flags=bicubic -c:v libx264 -preset fast -crf 22 -c:a copy #output.mp4
	# try nvidia
	# try faster seek
done <<< "$action_labels"
