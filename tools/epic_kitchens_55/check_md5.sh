#!/bin/bash

if [[ $# -lt 2 ]]
then
	echo "Usage: $0 [EPIC_KITCHENS_55_dir] [md5.csv]"
	echo "Download md5.csv from https://raw.githubusercontent.com/epic-kitchens/epic-kitchens-download-scripts/master/data/md5.csv"
	exit 1
fi


epic_dir="$1"
md5csv="$2"

md5file=$(cat "$md5csv" | grep ",55$" | awk -F, '{print $1" "$2}')

cd "$epic_dir"
md5sum -c <(echo "$md5file")
