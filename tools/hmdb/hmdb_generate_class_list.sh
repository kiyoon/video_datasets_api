#!/bin/bash

# Author: Kiyoon Kim (yoonkr33@gmail.com)
# Description: Split HMDB51 dataset with provided Three Splits text files.

if [ $# -lt 1 ]
then
	echo "Usage: $0 [Dataset location]"
	echo "Generate class key list"
	echo "Author: Kiyoon Kim (yoonkr33@gmail.com)"
	exit 0
fi

data_dir=$(realpath "$1")

classes=$(find "$data_dir" -mindepth 1 -maxdepth 1 -type d | sort)
if [ $(echo "$classes" | wc -l) -ne 51 ]
then
	echo "Error: dataset contains less or more than 51 classes." 1>&2
	exit 1
fi

echo "$classes" | xargs -i basename {} > classes.txt

