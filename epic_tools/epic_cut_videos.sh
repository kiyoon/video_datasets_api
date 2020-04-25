#!/bin/bash

timestamp() {
   date '+%s%N' --date="$1"
}
# timestamp "12:20:45.12345"  ==>  1485105645123450000

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

index=1

while read line
do
	id=$(echo "$line" | awk -F , '{print $1}')
	participant=$(echo "$line" | awk -F , '{print $2}')
	video=$(echo "$line" | awk -F , '{print $3}').MP4
	start_time=$(echo "$line" | awk -F , '{print $5}')
	end_time=$(echo "$line" | awk -F , '{print $6}')
	duration=$(( $(timestamp "$end_time") - $(timestamp "$start_time") ))
	duration_sec=$(echo "scale=2; $duration / 1000000000" | bc | awk '{printf "%.2f\n", $0}')		# awk: pad zero (.33 -> 0.33)
	verb=$(echo "$line" | awk -F , '{print $9}')

	echo $index / $num_segments
	
	#mkdir -p "$output_dir/$verb"
	# -copyts option ensures it cuts to the end_time, because we're using fast seek
	# DON'T use -copyts, as it may produce bug for (pyav) decoding.
	# setdar sets display aspect ratio to 1:1.
	# -r sets the output fps (30000/1001 means 29.97)
	#ffmpeg -ss $start_time -i "$input_dir/$participant/$video" -to $end_time -copyts -vf scale=256:256:flags=bicubic,setdar=1/1 -c:v libx264 -preset fast -crf 22 -an "$output_dir/$verb/$(printf '%05d' $id).mp4" < /dev/null 2> /dev/null
	#ffmpeg -ss $start_time -i "$input_dir/$participant/$video" -to $end_time -copyts -vf scale=-2:324 -sws_flags bicubic -c:v libx264 -preset fast -crf 22 -color_range pc -colorspace bt709 -color_trc bt709 -color_primaries bt709 -pix_fmt yuvj420p -an -r 15000/1001 "$output_dir/$(printf '%05d' $id).mp4" < /dev/null 2> /dev/null
	ffmpeg -ss $start_time -i "$input_dir/$participant/$video" -t $duration_sec -vf scale=-2:324 -sws_flags bicubic -c:v libx264 -preset fast -crf 22 -color_range pc -colorspace bt709 -color_trc bt709 -color_primaries bt709 -pix_fmt yuvj420p -an -r 15000/1001 "$output_dir/$(printf '%05d' $id).mp4" < /dev/null 2> /dev/null

	#ffmpeg -hwaccel cuvid -c:v h264_cuvid -ss $start_time -i "$input_dir/$participant/$video" -to $end_time -copyts -vf scale_npp=320:240 -c:v h264_nvenc -c:a copy "$output_dir/$verb/$(printf '%05d' $id).mp4" < /dev/null 2> /dev/null
	# normal: 6.52s after 30 segments
	# try nvidia: 0.74s after 40 segments, seems to be inaccurate
	# try fast and accurate seek: 0.786s after 40 segments

	bash_end_time=$(date +%s.%N)
	time_diff=$(echo "$bash_end_time - $bash_start_time" | bc)
	average_time=$(echo "$time_diff / ($index)" | bc -l)
	echo "average processing time per segment: $average_time"

	(( index++ ))
done <<< "$action_labels"
