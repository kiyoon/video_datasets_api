#!/bin/bash

if [ $# -lt 2 ]
then
	echo "usage: $0 [hmdb51_org.rar path] [extract_dir]"
	exit 1
fi

hmdb_rar="$1"
extract_dir="$2"

mkdir -p "$extract_dir"
unrar e "$hmdb_rar" "$extract_dir"

rarfiles=$(find "$extract_dir" -name "*.rar")

while read line
do
	class_dir="$extract_dir/$(basename "$line" .rar)"
	mkdir -p "$class_dir"
	unrar e "$line" "$class_dir"
done <<< "$rarfiles"

rm "$extract_dir/"*.rar
