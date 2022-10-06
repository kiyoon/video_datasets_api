#!/bin/bash

if [ $# -lt 6 ]
then
	echo "usage: $0 [videos_dir] [output_dir] [divide_job_count] [divide_job_index] [gpu_device] [gpu_arch (turing/pascal)]"
	echo "Extracts optical flow using docker."
	echo "divide_job_count > 1 will execute it to only part of the data. divide_job_index should be 0, 1, ..., divide_job_count-1"
	exit 1
fi

# Docker needs absolute path
input_dir="$(realpath $1)"
output_dir="$(realpath $2)"
divide_job_count="$3"
divide_job_index="$4"
gpu_device="$5"
gpu_arch="$6"


mkdir -p "$output_dir"

bash_start_time=$(date +%s.%N)


all_videos=$(find "$input_dir" -mindepth 2 -maxdepth 2 -name "*.avi" -type f | sort)
num_all_segments=$(echo "$all_videos" | wc -l)
num_part_segments="$((num_all_segments / divide_job_count))"


start_idx="$((divide_job_index * num_part_segments + 1))"
if [[ $divide_job_count -eq $((divide_job_index + 1)) ]]
then
	end_idx='$'
	# update number of segments because it is different for the last process.
	num_part_segments="$((num_all_segments / divide_job_count + num_all_segments % num_part_segments))"
else
	end_idx="$(( (divide_job_index+1) * num_part_segments ))"
fi

echo "all videos: $all_videos"
echo "Number of all videos: $num_all_segments"
echo "Number of videos to be processed: $num_part_segments"
echo "Video indices to be processed: $start_idx to $end_idx"
part_videos=$(echo "$all_videos" | sed -n "$start_idx,${end_idx}p")
first_video=$(echo "$part_videos" | head -1)
last_video=$(echo "$part_videos" | tail -1)
echo "Videos to be processed: $first_video to $last_video"

num_errors=0
error_videos=""

index=1
while read line
do
	echo $index / $num_part_segments

	video_name=$(basename "$line")
	video_dir=$(dirname "$line")
	
	relative_path=$(realpath --relative-to="$input_dir" "$line")
	relative_dir=$(dirname "$relative_path")
	echo "$relative_path"

	mkdir -p "$output_dir/$relative_dir"
	docker run --gpus "device=$gpu_device" --rm -u $UID:$UID -v "$video_dir:/input" -v "$output_dir/$relative_dir:/output" kiyoon/denseflow:$gpu_arch "/input/$video_name" -b=20 -a=tvl1 -s=1 -v -o=/output
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
	num_videos_left=$((num_part_segments - index))
	eta=$(echo "$num_videos_left * ($average_time)" | bc -l)
	printf "Average processing time per segment: %.2f, ETA: %.0f\n" "$average_time" "$eta"

	(( index++ ))
done <<< "$part_videos"

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
