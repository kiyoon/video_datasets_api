#!/bin/bash

download_and_extract() {
	subject_id="$1"
	output_dir="$2"
	filename="S${subject_id}_Brownie_Video.zip"
	wget --content-disposition "http://kitchen.cs.cmu.edu/Main/$filename" -P "$output_dir"
	unzip "$output_dir/$filename" -d "$output_dir"
	#rm "$output_dir/$filename"
}

if [[ $# -lt 1 ]]
then
	echo "Usage: $0 [output_dir]"
	echo "Download CMU-MMAC dataset but only the action recognition part."
	exit 1
fi

output_dir="$1"
mkdir -p "$output_dir"

for subject_id in 06 10 23
do
	download_halfres $subject_id "$output_dir"
done 

for subject_id in 07 08 09 12 13 14 16 17 18 19 20 22 24
do
	download_and_extract $subject_id "$output_dir"
done 

