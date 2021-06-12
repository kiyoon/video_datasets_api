#!/bin/bash

if [ $# -ne 2 ]
then
	echo "Usage: $0 [dir_with_subtars] [output_dir]"
	exit 1
fi

dir_with_subtars="$1"
output_dir="$2"


subtars=$(find "$dir_with_subtars" -name "*.tar" -type f)
mkdir -p "$output_dir"

while read line
do
	class_name=$(basename "$line" .tar)
	echo "$class_name"
	mkdir "$output_dir/$class_name"
	tar xf "$line" -C "$output_dir/$class_name"
done <<< "$subtars"
