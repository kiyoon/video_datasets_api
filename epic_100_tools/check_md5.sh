#!/bin/bash

if [[ $# -lt 2 ]]
then
	echo "Usage: $0 [EPIC_KITCHENS_100_dir] [md5.csv]"
	echo "Download md5.csv from https://raw.githubusercontent.com/epic-kitchens/epic-kitchens-download-scripts/master/data/md5.csv"
	exit 1
fi


epic_dir="$1"
md5csv="$2"

md5file=$(cat "$md5csv" | grep ",100$" | awk -F, '{print $1" "$2}')
md5file_errata=$(cat "$md5csv" | grep ",errata$" | awk -F, '{print $1" "$2}')

cd "$epic_dir"
md5sum -c <(echo "$md5file")

echo "Checking errata"
md5sum -c <(echo "$md5file_errata")
