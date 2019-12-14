
from . import label_map_util
import csv

def EPIC_read_noun_labels(label_path):
    input_file = csv.DictReader(open(label_path))

    labels = []
    for row in input_file:
        labels.append(row['class_key'])

    return labels
    

def EPIC_read_noun_labels_to_category_index(label_path):
    """This function reads the epic-kitchens noun csv and returns a list of dicts, each of
  which  has the following keys:
    'id': (required) an integer id uniquely identifying this category.
    'name': (required) string representing category name
      e.g., 'cat', 'dog', 'pizza'.
    """

    input_file = csv.DictReader(open(label_path))

    categories = []
    for row in input_file:
        categories.append({'id': int(row['noun_id']), 'name': row['class_key']})

    return label_map_util.create_category_index(categories)
