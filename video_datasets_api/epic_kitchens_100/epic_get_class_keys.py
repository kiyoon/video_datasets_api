import pandas as pd

def EPIC100_get_class_keys(epic_classes_csv):
    """Get class keys (verb or noun) 

    Returns:
        pandas dataframe (list of strings)
    """
    class_keys = pd.read_csv(epic_classes_csv, quotechar='"', skipinitialspace=True)['key']
    return class_keys
