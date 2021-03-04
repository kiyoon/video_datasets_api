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

index=1

avis=$(find "$1" -name "*.mp4")
num_segments=$(echo "$avis" | wc -l)

while read line
do
	echo $index / $num_segments

	frames_dir="${line/$input_dir/$output_dir}"
	
	mkdir -p "$frames_dir"
	# -copyts option ensures it cuts to the end_time, because we're using fast seek
	# DON'T use -copyts, as it may produce bug for (pyav) decoding.
	# setdar sets display aspect ratio to 1:1.
	# -r sets the output fps (30000/1001 means 29.97)
	ffmpeg -i "$line" -start_number 0 "$frames_dir/%05d.jpg" < /dev/null 2> /dev/null
	

	#ffmpeg -hwaccel cuvid -c:v h264_cuvid -ss $start_time -i "$input_dir/$participant/$video" -to $end_time -copyts -vf scale_npp=320:240 -c:v h264_nvenc -c:a copy "$output_dir/$verb/$(printf '%05d' $id).mp4" < /dev/null 2> /dev/null
	# normal: 6.52s after 30 segments
	# try nvidia: 0.74s after 40 segments, seems to be inaccurate
	# try fast and accurate seek: 0.786s after 40 segments

	bash_end_time=$(date +%s.%N)
	time_diff=$(echo "$bash_end_time - $bash_start_time" | bc)
	average_time=$(echo "$time_diff / ($index)" | bc -l)
	echo "average processing time per segment: $average_time"

	(( index++ ))
done <<< "$avis"
