import pandas as pd
import os

from .definitions import verb_category_str_to_index, noun_category_str_to_index

def EPIC100_get_class_keys(annotations_root_dir: str, verbnoun = 'verb'):
    """Get class keys (verb or noun) 

    Returns:
        pandas dataframe (list of strings)
    """
    assert verbnoun in ['verb', 'noun']
    
    class_keys = pd.read_csv(os.path.join(annotations_root_dir, f'EPIC_100_{verbnoun}_classes.csv'), quotechar='"', skipinitialspace=True)['key']
    return class_keys


def EPIC100_get_class_label_to_category_index(annotations_root_dir: str, verbnoun = 'verb'):
    """Get class groups (verb or noun) 

    Returns:
        pandas dataframe (list of strings)
    """
    assert verbnoun in ['verb', 'noun']
    if verbnoun == 'verb':
        category_str_to_index = verb_category_str_to_index
    else:
        category_str_to_index = noun_category_str_to_index
    
    classes = pd.read_csv(os.path.join(annotations_root_dir, f'EPIC_100_{verbnoun}_classes.csv'), quotechar='"', skipinitialspace=True)

    class_to_category = []
    for index, row in classes.iterrows():
        assert index == int(row['id'])
        class_to_category.append(category_str_to_index[row['category']])

    return class_to_category
