import pandas as pd
import os

def EPIC100_get_class_keys(annotations_root_dir: str, verbnoun = 'verb'):
    """Get class keys (verb or noun) 

    Returns:
        pandas dataframe (list of strings)
    """
    assert verbnoun in ['verb', 'noun']
    
    class_keys = pd.read_csv(os.path.join(annotations_root_dir, f'EPIC_100_{verbnoun}_classes.csv'), quotechar='"', skipinitialspace=True)['key']
    return class_keys
