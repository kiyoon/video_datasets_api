#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 [download_dir]"
	exit 1
fi

if ! command -v unrar &> /dev/null
then
	echo "unrar could not be found"
	exit
fi

script_dir="$(dirname $0)"
download_dir="$1"

mkdir -p "$download_dir"

echo "Downloading video data"
wget 'http://serre-lab.clps.brown.edu/wp-content/uploads/2013/10/hmdb51_org.rar' -O "$download_dir/hmdb51_org.rar"
 
echo "Extracting video data"
bash "$script_dir/hmdb_extract_rar.sh" "$download_dir/hmdb51_org.rar" "$download_dir/videos"

echo "Removing video rar"
rm "$download_dir/hmdb51_org.rar"

echo "Downloading splits"
wget 'http://serre-lab.clps.brown.edu/wp-content/uploads/2013/10/test_train_splits.rar' -O "$download_dir/test_train_splits.rar"

echo "Extracting splits"
unrar x "$download_dir/test_train_splits.rar" "$download_dir"
echo "Removing splits rar"
rm "$download_dir/test_train_splits.rar"
