#!/bin/bash

if [ $# -lt 4 ]
then
	echo "usage: $0 [frames_dir] [output_dir] [gpu_arch (turing/pascal)] [gpu_devices..]"
	echo "Extracts optical flow using docker."
	echo "Videos has to be extracted as frames."
	echo "It will create a tmux session and execute multiple processes to process different parts of the dataset."
	exit 1
fi

script_dir=$(dirname "$(realpath -s "$0")")
input_dir="$1"
output_dir="$2"
gpu_arch="$3"
gpu_devices=( "${@:4}" )
num_gpus=${#gpu_devices[@]}

sess="flow_multigpu"

tmux new -d -s "$sess" -c "$script_dir"		# create new session, default directory to script directory

for (( window=0; window<$num_gpus; window++ ))
do
	tmux new-window -t "$sess:$window"

	command="bash $script_dir/extract_flow_partition.sh '$input_dir' '$output_dir' $num_gpus $window ${gpu_devices[$window]} $gpu_arch"
    tmux send-keys -t "$sess:$window" "$command" Enter
done


echo "Flow extracting.. Open screen by 'tmux a -t $sess'"
