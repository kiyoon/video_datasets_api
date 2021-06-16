#!/bin/bash

if [ $# -lt 1 ]
then
	echo "Usage: $0 [download_dir]"
	echo "It will download max2action and max2action_cameramotion and extract them."
	exit 1

fi


download_dir="$1"


mkdir -p "$download_dir"
mkdir -p "$download_dir/max2action"
mkdir -p "$download_dir/max2action_cameramotion"

wget 'https://cmu.box.com/shared/static/jgbch9enrcfvxtwkrqsdbitwvuwnopl0.zip' -O "$download_dir/max2action/videos.zip"
unzip "$download_dir/max2action/videos.zip" -d "$download_dir/max2action"
rm "$download_dir/max2action/videos.zip"
wget 'https://cmu.box.com/shared/static/922x4qs3feynstjj42muecrlch1o7pmv.zip' -O "$download_dir/max2action/scenes.zip"
unzip "$download_dir/max2action/scenes.zip" -d "$download_dir/max2action"
rm "$download_dir/max2action/scenes.zip"
wget 'https://cmu.box.com/shared/static/7svgta3kqat1jhe9kp0zuptt3vrvarzw.zip' -O "$download_dir/max2action/lists.zip"
unzip "$download_dir/max2action/lists.zip" -d "$download_dir/max2action"
rm "$download_dir/max2action/lists.zip"

wget 'https://cmu.box.com/shared/static/yvhx9p5haip5abzh9i2fofssjpq34zwz.zip' -O "$download_dir/max2action_cameramotion/videos.zip"
unzip "$download_dir/max2action_cameramotion/videos.zip" -d "$download_dir/max2action_cameramotion"
rm "$download_dir/max2action_cameramotion/videos.zip"
wget 'https://cmu.box.com/shared/static/zfau8j1e6n7ylobf0g1d2wjdgdu86j2e.zip' -O "$download_dir/max2action_cameramotion/scenes.zip"
unzip "$download_dir/max2action_cameramotion/scenes.zip" -d "$download_dir/max2action_cameramotion"
rm "$download_dir/max2action_cameramotion/scenes.zip"
wget 'https://cmu.box.com/shared/static/i9kexj33if00t338esnw93uzm5f6sfar.zip' -O "$download_dir/max2action_cameramotion/lists.zip"
unzip "$download_dir/max2action_cameramotion/lists.zip" -d "$download_dir/max2action_cameramotion"
rm "$download_dir/max2action_cameramotion/lists.zip"


