import pandas as pd

def EPIC_get_verb_class_keys(epic_verb_classes_csv):
    """Get class keys 

    Returns:
        pandas dataframe (list of strings)
    """
    class_keys = pd.read_csv(epic_verb_classes_csv, quotechar='"', skipinitialspace=True)['class_key']
    return class_keys
