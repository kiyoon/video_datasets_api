NUM_VERB_CLASSES = 97
NUM_NOUN_CLASSES = 300


# The ordering follows the official website's (https://epic-kitchens.github.io/2022) stats graph.
verb_categories = ['retrieve', 'leave', 'clean', 'access', 'block', 'merge', 'split', 'manipulate', 'transition', 'monitor', 'sense', 'distribute', 'other']
noun_categories = ['appliances', 'crockery', 'containers', 'cutlery', 'vegetables', 'cookware', 'utensils', 'furniture', 'cleaning', 'storage', 'baked goods and grains', 'spices and herbs and sauces', 'materials', 'meat and substitutes', 'rubbish', 'dairy and eggs', 'prepared food', 'hand', 'drinks', 'fruits and nuts', 'other']


NUM_VERB_CATEGORIES = len(verb_categories)
NUM_NOUN_CATEGORIES = len(noun_categories)

verb_category_str_to_index = {}
for idx, category in enumerate(verb_categories):
    verb_category_str_to_index[category] = idx

noun_category_str_to_index = {}
for idx, category in enumerate(noun_categories):
    noun_category_str_to_index[category] = idx

