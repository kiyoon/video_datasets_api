import pandas
import pickle

def epic_narration_id_to_unique_id(annotations_root_dir: str):
    def sort_narration_id(narration_id: str):
        list_narration = narration_id.replace('P', '', 1).split('_')
        list_narration[0] = int(list_narration[0])
        list_narration[1] = int(list_narration[1])
        list_narration[2] = int(list_narration[2])
        return list_narration

    train_pkl = os.path.join(annotations_root_dir, 'EPIC_100_train.pkl')
    val_pkl = os.path.join(annotations_root_dir, 'EPIC_100_validation.pkl')
    test_pkl = os.path.join(annotations_root_dir, 'EPIC_100_test_timestamps.pkl')

    with open(train_pkl, 'rb') as f:
        train_labels = pickle.load(f)
    
    narration_ids_sorted = sorted(train_labels.index, key = sort_narration_id)

    with open(val_pkl, 'rb') as f:
        val_labels = pickle.load(f)

    val_narration_ids = sorted(val_labels.index, key = sort_narration_id)
    narration_ids_sorted.extend(val_narration_ids)

    with open(test_pkl, 'rb') as f:
        test_labels = pickle.load(f)

    test_narration_ids = sorted(test_labels.index, key = sort_narration_id)
    narration_ids_sorted.extend(test_narration_ids)

    narration_id_to_video_id = {narration_id: uid for uid, narration_id in enumerate(narration_ids_sorted)}

    return narration_id_to_video_id, narration_ids_sorted



def get_verb_uid2label_dict(annotations_rood_dir: str, narration_id_to_video_id = None):
    train_pkl = os.path.join(annotations_root_dir, 'EPIC_100_train.pkl')
    val_pkl = os.path.join(annotations_root_dir, 'EPIC_100_validation.pkl')

    if narration_id_to_video_id is None:
        narration_id_to_video_id, _ = epic_narration_id_to_unique_id(annotations_root_dir)

    uid2label = {}

    with open(train_pkl, 'rb') as f:
        train_labels = pickle.load(f)
    
    num_videos = len(train_labels.index)
    for index in range(num_videos):
        narration_id = train_labels.index.iloc[index]
        uid = narration_id_to_video_id[narration_id]
        verb_label = train_labels.verb_class.iloc[index]

        uid2label[uid] = verb_label

    with open(val_pkl, 'rb') as f:
        val_labels = pickle.load(f)

    num_videos = len(val_labels.index)
    for index in range(num_videos):
        narration_id = val_labels.index.iloc[index]
        uid = narration_id_to_video_id[narration_id]
        verb_label = val_labels.verb_class.iloc[index]

        uid2label[uid] = verb_label

    return uid2label
