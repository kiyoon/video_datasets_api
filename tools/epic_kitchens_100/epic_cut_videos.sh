#!/bin/bash

timestamp() {
   date '+%s%N' --date="$1"
}
# timestamp "12:20:45.12345"  ==>  1485105645123450000

if [ $# -lt 4 ]
then
	echo "usage: $0 [input_dir_55 (should be .../videos containing train and test folder)] [input_dir_extension] [output_dir] [annotations_root_dir]"
	echo "EPIC-55 and 100 have different directory structure. You can put two input directories (55 and extension), or just put same directory if you have them combined."
	exit 1
fi

input_dir_55="$1"
input_dir_extension="$2"
output_dir="$3"
annotations_root_dir="$4"

train_labels=$(cat "$annotations_root_dir/EPIC_100_train.csv" | sed 1d)
val_labels=$(cat "$annotations_root_dir/EPIC_100_validation.csv" | sed 1d)
train_num_segments=$(echo "$train_labels" | wc -l)
val_num_segments=$(echo "$val_labels" | wc -l)
num_segments=$((train_num_segments+val_num_segments))

bash_start_time=$(date +%s.%N)

index=1

num_errors=0
error_videos=""


for split in train val
do
	if [[ "$split" == "train" ]]
	then
		action_labels="$train_labels"
	elif [[ "$split" == "val" ]]
	then
		action_labels="$val_labels"
	fi

	mkdir -p "$output_dir/$split"

	while read line
	do
		id=$(echo "$line" | awk -F , '{print $1}')
		participant=$(echo "$line" | awk -F , '{print $2}')
		video=$(echo "$line" | awk -F , '{print $3}').MP4
		start_time=$(echo "$line" | awk -F , '{print $5}')
		end_time=$(echo "$line" | awk -F , '{print $6}')
		duration=$(( $(timestamp "$end_time") - $(timestamp "$start_time") ))
		duration_sec=$(echo "scale=2; $duration / 1000000000" | bc | awk '{printf "%.2f\n", $0}')		# awk: pad zero (.33 -> 0.33)

		echo $index / $num_segments
		
		if [[ -f "$input_dir_55/train/$participant/$video" ]]
		then
			video_path="$input_dir_55/train/$participant/$video"
		elif [[ -f "$input_dir_55/test/$participant/$video" ]]
		then
			video_path="$input_dir_55/test/$participant/$video"
		elif [[ -f "$input_dir_extension/$participant/videos/$video" ]]
		then
			video_path="$input_dir_extension/$participant/videos/$video"
		else
			printf '\xF0\x9F\x98\xAD'	# loudly crying face
			echo " ERROR COULDN'T FIND THE VIDEO $video"
			(( num_errors += 1 ))
			error_videos="$error_videos$line\n"
			continue
		fi

		output_path="$output_dir/$split/$id.mp4"
		echo "Using $video_path -> Output $output_path"
		
		ffmpeg -ss $start_time -i "$video_path" -t $duration_sec -vf scale=-2:324 -sws_flags bicubic -c:v libx264 -preset fast -crf 22 -color_range pc -colorspace bt709 -color_trc bt709 -color_primaries bt709 -pix_fmt yuvj420p -an -r 15000/1001 "$output_path" < /dev/null 2> /dev/null

		#ffmpeg -hwaccel cuvid -c:v h264_cuvid -ss $start_time -i "$input_dir/$participant/$video" -to $end_time -copyts -vf scale_npp=320:240 -c:v h264_nvenc -c:a copy "$output_dir/$verb/$(printf '%05d' $id).mp4" < /dev/null 2> /dev/null
		# normal: 6.52s after 30 segments
		# try nvidia: 0.74s after 40 segments, seems to be inaccurate
		# try fast and accurate seek: 0.786s after 40 segments

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
		echo "average processing time per segment: $average_time"

		(( index++ ))
	done <<< "$action_labels"
done


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
