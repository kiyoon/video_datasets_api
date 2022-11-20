#!/bin/bash

if [ $# -lt 5 ]
then
	echo "usage: $0 [frames_dir] [output_dir] [denseflow_step] [gpu_arch (ampere(30xx)/turing(20xx)/pascal(10xx))] [jobs_per_gpu] [gpu_devices..] "
	echo "Extracts optical flow using docker."
	echo "Videos has to be extracted as frames."
	echo "It will create a tmux session and execute multiple processes to process different parts of the dataset."
	echo "Running multiple jobs per gpu makes it dramatically faster."
	echo "It supports saving the progress and skipping all files that are already processed."
	exit 1
fi

script_dir=$(dirname "$(realpath -s "$0")")
input_dir="$1"
output_dir="$2"
denseflow_step="$3"
gpu_arch="$4"
jobs_per_gpu="$5"
gpu_devices=( "${@:6}" )
num_gpus=${#gpu_devices[@]}

sess="flow_multigpu"

tmux new -d -s "$sess" -c "$script_dir"		# create new session, default directory to script directory

for (( gpuid=0; gpuid<$num_gpus; gpuid++ ))
do
	for (( jobid=0; jobid<$jobs_per_gpu; jobid++ ))
	do
		window="$((gpuid*jobs_per_gpu+jobid))"
		tmux new-window -t "$sess:$window"

		command="bash $script_dir/extract_flow_partition.sh '$input_dir' '$output_dir' $denseflow_step $((num_gpus*jobs_per_gpu)) $window ${gpu_devices[$gpuid]} $gpu_arch"
		tmux send-keys -t "$sess:$window" "$command" Enter
	done
done


echo "Flow extracting.. Open screen by 'tmux a -t $sess'"
