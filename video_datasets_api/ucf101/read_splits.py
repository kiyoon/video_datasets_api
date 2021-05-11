def read_train_test_splits(traintestlist_txt_path: str, class_keys_to_indices: dict) -> list:
    """
    Return:
        list of tuple (path, class_label_index)
    """
    split_list = []
    with open(traintestlist_txt_path, "r") as f:
        for line in f.readlines():
            path = line.split(" ")[0].strip()   # ignoring the labels provided.
            class_key = path.split("/")[0]
            split_list.append((path, class_keys_to_indices[class_key]))

    return split_list

