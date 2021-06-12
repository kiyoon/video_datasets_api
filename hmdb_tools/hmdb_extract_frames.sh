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

avis=$(find "$1" -name "*.avi")
num_segments=$(echo "$avis" | wc -l)

while read line
do
	echo $index / $num_segments

	frames_dir="${line/$input_dir/$output_dir}"
	
	mkdir -p "$frames_dir"
	# -qscale:v : 1~31 where 31 is the worst quality
	# when -qscale:v == 1, -qmin 1 need to be added
	ffmpeg -i "$line" -start_number 0 -qscale:v "$quality" "$frames_dir/%05d.jpg" < /dev/null 2> /dev/null

	bash_end_time=$(date +%s.%N)
	time_diff=$(echo "$bash_end_time - $bash_start_time" | bc)
	average_time=$(echo "$time_diff / ($index)" | bc -l)
	echo "average processing time per segment: $average_time"

	(( index++ ))
done <<< "$avis"
