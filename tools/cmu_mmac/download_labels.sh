#!/bin/bash

download_and_extract() {
	subject_id="$1"
	output_dir="$2"
	filename="S${subject_id}_Brownie.zip"
	wget --content-disposition "http://www.cs.cmu.edu/~espriggs/cmu-mmac/annotations/files/$filename" -P "$output_dir"
	unzip "$output_dir/$filename" -d "$output_dir"
	rm "$output_dir/$filename"
}

if [[ $# -lt 1 ]]
then
	echo "Usage: $0 [output_dir]"
	echo "Download CMU-MMAC dataset but only the action recognition part."
	exit 1
fi

output_dir="$1"
mkdir -p "$output_dir"

for subject_id in 06 07 08 09 10 12 13 14 16 17 18 19 20 22 23 24
do
	download_and_extract $subject_id "$output_dir"
done 
