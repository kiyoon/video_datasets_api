import pandas
import pickle

def get_verb_uid2label_dict(train_action_labels_pkl):
    with open(train_action_labels_pkl, 'rb') as f:
        epic_action_labels = pickle.load(f)

    uid2label = {}
    
    num_videos = len(epic_action_labels.index)
    for index in range(num_videos):
        uid = epic_action_labels.index[index]
        verb_label = epic_action_labels.verb_class.iloc[index]

        uid2label[uid] = verb_label

    return uid2label
