#!/bin/bash

if [[ $# -lt 1 ]]
then
	echo "Usage: $0 [output_dir]"
	exit 1
fi

output_dir="$1"
mkdir -p "$output_dir"

wget --content-disposition https://www.dropbox.com/s/ms1z1z8iqi997yp/GTEA_Gaze_Plus_labels_cleaned.zip?dl=1 -P "$output_dir"
unzip "$output_dir/GTEA_Gaze_Plus_labels_cleaned.zip" -d "$output_dir"
rm "$output_dir/GTEA_Gaze_Plus_labels_cleaned.zip"
