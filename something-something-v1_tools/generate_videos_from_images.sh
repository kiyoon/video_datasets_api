#!/bin/bash

if [ $# -lt 2 ]
then
	echo "usage: $0 [input_dir] [output_dir]"
	exit 1
fi

input_dir="$1"
output_dir="$2"

mkdir -p "$output_dir"

bash_start_time=$(date +%s.%N)
for i in {1..108499}
do
	echo $i / 108499

	ffmpeg -start_number 1 -i "$input_dir/$i/%05d.jpg" -vf scale=256:256:flags=bicubic,setdar=1/1,fps=12 -c:v libx264 -preset fast -crf 22 -an -pix_fmt yuv420p "$output_dir/$(printf '%06d' $i).mp4" < /dev/null 2> /dev/null

	bash_end_time=$(date +%s.%N)
	time_diff=$(echo "$bash_end_time - $bash_start_time" | bc)
	average_time=$(echo "$time_diff / ($i)" | bc -l)
	echo "average processing time per segment: $average_time"
done
