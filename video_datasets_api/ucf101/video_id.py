import os 

def get_unique_video_ids_from_videos(videos_dir: str, search_dirs: bool = False) -> dict:
    videos_dir = os.path.join(videos_dir, '')
    video_list = []
    video_path_to_ids = {}
    current_video_id = 0
    for root, dirs, files in os.walk(videos_dir):
        dirs.sort()
        files.sort()
        if search_dirs:
            search_list = dirs
        else:
            search_list = files

        for name in search_list:
            if name.endswith(".avi"):
                name_relative = os.path.join(root.replace(videos_dir, ''), name)
                video_list.append(name_relative)
                video_path_to_ids[name_relative] = current_video_id
                current_video_id += 1

    return video_list, video_path_to_ids

