#!/bin/bash

if [ $# -lt 3 ]
then
	echo "usage: $0 [input_dir (should be .../videos/train)] [output_dir] [EPIC_train_action_labels.csv]"
	exit 1
fi

input_dir="$1"
output_dir="$2"
action_labels_csv="$3"

action_labels=$(cat "$action_labels_csv" | sed 1d)
num_segments=$(echo "$action_labels" | wc -l)

mkdir -p "$output_dir"

bash_start_time=$(date +%s.%N)

while read line
do
	id=$(echo "$line" | awk -F , '{print $1}')
	participant=$(echo "$line" | awk -F , '{print $2}')
	video=$(echo "$line" | awk -F , '{print $3}').MP4
	start_time=$(echo "$line" | awk -F , '{print $5}')
	end_time=$(echo "$line" | awk -F , '{print $6}')
	verb=$(echo "$line" | awk -F , '{print $9}')

	echo $((id + 1)) / $num_segments
	
	mkdir -p "$output_dir/$verb"
	ffmpeg -ss $start_time -i "$input_dir/$participant/$video" -to $end_time -copyts -vf scale=320:240:flags=bicubic -c:v libx264 -preset fast -crf 22 -c:a copy "$output_dir/$verb/$(printf '%05d' $id).mp4" < /dev/null 2> /dev/null

	#ffmpeg -hwaccel cuvid -c:v h264_cuvid -ss $start_time -i "$input_dir/$participant/$video" -to $end_time -copyts -vf scale_npp=320:240 -c:v h264_nvenc -c:a copy "$output_dir/$verb/$(printf '%05d' $id).mp4" < /dev/null 2> /dev/null
	# normal: 6.52s after 30 segments
	# try nvidia: 0.74s after 40 segments
	# try fast and accurate seek: 0.786s after 40 segments

	bash_end_time=$(date +%s.%N)
	time_diff=$(echo "$bash_end_time - $bash_start_time" | bc)
	average_time=$(echo "$time_diff / ($id+1)" | bc -l)
	echo "average processing time per segment: $average_time"
done <<< "$action_labels"
