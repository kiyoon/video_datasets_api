#!/bin/bash

if [ $# -lt 2 ]
then
	echo "usage: $0 [input_dir] [output_dir] [quality=5 (2(best)-31(worst))]"
	exit 1
fi

input_dir="$1"
output_dir="$2"

if [ $# -eq 2 ]
then
	quality=5
else
	quality="$3"
fi

mkdir -p "$output_dir"

bash_start_time=$(date +%s.%N)

index=1

videos=$(find "$1" -name "*.avi")
num_segments=$(echo "$videos" | wc -l)

num_errors=0
error_videos=""

while read line
do
	echo $index / $num_segments

	path_wo_ext="${line%.avi}"
	frames_dir="${path_wo_ext/$input_dir/$output_dir}"
	echo $frames_dir
	
	mkdir -p "$frames_dir"
	# -qscale:v : 1~31 where 31 is the worst quality
	# when -qscale:v == 1, -qmin 1 need to be added
	ffmpeg -i "$line" -start_number 1 -qscale:v "$quality" "$frames_dir/%05d.jpg" < /dev/null 2> /dev/null
	RC=$?
	if [ "${RC}" -ne "0" ]; then
		# Do something to handle the error.
		printf '\xF0\x9F\x98\xAD'	# loudly crying face
		echo " ERROR OCCURED WHILE PROCESSING THE VIDEO"
		(( num_errors += 1 ))
		error_videos="$error_videos$line\n"
	fi

	bash_end_time=$(date +%s.%N)
	time_diff=$(echo "$bash_end_time - $bash_start_time" | bc)
	average_time=$(echo "$time_diff / ($index)" | bc -l)
	num_videos_left=$((num_segments - index))
	eta=$(echo "$num_videos_left * ($average_time)" | bc -l)
	printf "Average processing time per segment: %.2f, ETA: %.0f\n" "$average_time" "$eta"

	(( index++ ))
done <<< "$videos"

if [ $num_errors -gt 0 ]
then
	printf '\xF0\x9F\x98\xA1'	# pouting face
	echo " $num_errors errors occurred whilst extracting videos."
	echo "Failed list:"
	printf "$error_videos"
else
	printf '\xF0\x9F\x98\x8D'	# smiling face with heart-shaped eyes
	echo " All videos successfully extracted"
fi
