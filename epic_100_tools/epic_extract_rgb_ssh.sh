#!/bin/bash

if [[ $# -lt 5 ]]
then
	echo "Usage: $0 [ssh hostname] [EPIC-55 dir] [EPIC-100 extensions dir] [output_dir] [md5.csv]"
	echo "Find tar file from a remote SSH server, either of the two directory structures, and extract them in one location."
	echo "Download md5.csv from https://raw.githubusercontent.com/epic-kitchens/epic-kitchens-download-scripts/master/data/md5.csv"
	exit 1
fi

ssh_hostname="$1"
epic55_dir="$2"
epic100_dir="$3"
output_dir="$4"
md5_csv="$5"


epic55_rgb_tars=$(cat "$md5_csv" | grep /rgb/ | awk -F, '{print $2}' | sort)
epic100_rgb_tars=$(cat "$md5_csv" | grep /rgb_frames/ | awk -F, '{print $2}' | sort)


num_errors=0
error_videos=""

while read tarfile
do
	participant=$(echo "$tarfile" | awk -F/ '{print $4}')
	videoid=$(echo "$tarfile" | awk -F/ '{print $5}' | awk -F. '{print $1}')
	extract_dir="$output_dir/$participant/$videoid"
	echo "Extracting $ssh_hostname:$epic55_dir/$tarfile to $extract_dir"
	mkdir -p "$extract_dir"
	if ssh -n "$ssh_hostname" "cat '$epic55_dir/$tarfile'" | tar xf - -C "$extract_dir"
	then
		true
	else
		printf '\xF0\x9F\x98\xAD'	# loudly crying face
		echo " ERROR OCCURED WHILE EXTRACTING TAR"
		(( num_errors += 1 ))
		error_videos="$error_videos$tarfile\n"
	fi
	
done <<< "$epic55_rgb_tars"

while read tarfile
do
	participant=$(echo "$tarfile" | awk -F/ '{print $1}')
	videoid=$(echo "$tarfile" | awk -F/ '{print $3}' | awk -F. '{print $1}')
	extract_dir="$output_dir/$participant/$videoid"
	echo "Extracting $ssh_hostname:$epic100_dir/$tarfile to $extract_dir"
	mkdir -p "$extract_dir"
	if ssh -n "$ssh_hostname" "cat '$epic100_dir/$tarfile'" | tar xf - -C "$extract_dir"
	then
		true
	else
		printf '\xF0\x9F\x98\xAD'	# loudly crying face
		echo " ERROR OCCURED WHILE EXTRACTING TAR"
		(( num_errors += 1 ))
		error_videos="$error_videos$tarfile\n"
	fi
	
done <<< "$epic100_rgb_tars"


if [ $num_errors -gt 0 ]
then
	printf '\xF0\x9F\x98\xA1'	# pouting face
	echo " $num_errors errors occurred whilst extracting tar files."
	echo "Failed list:"
	printf "$error_videos"
else
	printf '\xF0\x9F\x98\x8D'	# smiling face with heart-shaped eyes
	echo " All tar files successfully extracted"
fi
