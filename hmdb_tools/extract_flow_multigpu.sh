#!/bin/bash

if [ $# -lt 5 ]
then
	echo "usage: $0 [frames_dir] [output_dir] [gpu_devices..]"
	echo "Extracts optical flow using docker."
	echo "Frames has to be extracted as frames and the directory name should end with '.avi'."
	echo "It will create a screen session and execute multiple processes to process different parts of the dataset."
	exit 1
fi

input_dir="$1"
output_dir="$2"
gpu_devices=( "${@:3}" )
num_gpus=${#gpu_devices[@]}

sess="flow_multigpu"

screen -dmS "$sess"

for (( window=0; window<$num_gpus; window++ ))
do
    # Window 0 already exists so don't make it again
    if [ $window -ne 0 ]
    then
        screen -S "$sess" -X screen $window
    fi

	command="bash extract_flow_partition.sh '$input_dir' '$output_dir' $num_gpus $window ${gpu_devices[$window]}\n"
    screen -S "$sess" -p $window -X stuff "$command"
done


echo "Flow extracting.. Open screen by 'screen -r $sess'"
