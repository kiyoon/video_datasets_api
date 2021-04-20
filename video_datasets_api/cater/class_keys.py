from itertools import permutations, product

ACTION_CLASSES = [
    # object, movement
    ('sphere', '_slide'),
    ('sphere', '_pick_place'),
    ('spl', '_slide'),
    ('spl', '_pick_place'),
    ('spl', '_rotate'),
    ('cylinder', '_pick_place'),
    ('cylinder', '_slide'),
    ('cylinder', '_rotate'),
    ('cube', '_slide'),
    ('cube', '_pick_place'),
    ('cube', '_rotate'),
    ('cone', '_contain'),
    ('cone', '_pick_place'),
    ('cone', '_slide'),
]
_BEFORE = 'before'
_AFTER = 'after'
_DURING = 'during'
ORDERING = [
    _BEFORE,
    _DURING,
    _AFTER,
]

ACTIONS = ['_slide', '_pick_place', '_rotate', '_contain']
OBJECTS = ['sphere', 'spl', 'cylinder', 'cube', 'cone']



def reverse(el):
    if el == ('during',):
        return el
    elif el == ('before',):
        return ('after',)
    elif el == ('after',):
        return ('before',)
    else:
        raise ValueError(f'el is {el}. This should not happen')

def action_order_unique(classes, only_before=False):
    classes_uniq = []
    for el in classes:
        if el not in classes_uniq and ((el[0][1], el[0][0]), reverse(el[1])) not in classes_uniq:
            if only_before and el[1] == ('after',):
                classes_uniq.append(((el[0][1], el[0][0]), reverse(el[1])))
            else:
                classes_uniq.append(el)
    return classes_uniq


def class_keys_task1(string=True):
    classes = ACTION_CLASSES

    if string:
        classes = [x[0] + x[1] for x in classes]
        return classes

    else:
        return classes

def class_to_string(class_, return_duplicate=False):
    if return_duplicate:
        return (class_[0][0][0] + class_[0][0][1] + ' ' + class_[1][0] + ' ' + class_[0][1][0] + class_[0][1][1],
                class_[0][1][0] + class_[0][1][1] + ' ' + reverse(class_[1])[0] + ' ' + class_[0][0][0] + class_[0][0][1])
    else:
        return class_[0][0][0] + class_[0][0][1] + ' ' + class_[1][0] + ' ' + class_[0][1][0] + class_[0][1][1]

def class_keys_task2(n=2, unique=True, string=True, only_before=False):
    """
    params:
        only_before (bool): if True, convert all "after" to "before".
    """
    action_sets = list(product(ACTION_CLASSES, repeat=n))
    # all orderings
    orderings = list(product(ORDERING, repeat=(n-1)))
    # all actions and orderings
    classes = list(product(action_sets, orderings))
    if unique:
        # Remove classes such as "X before Y" when "Y after X" already exists in the data
        classes = action_order_unique(classes, only_before=only_before)

    if string:
        classes = [class_to_string(x, False) for x in classes]
        return classes

    else:
        return classes


def class_keys_to_labels(class_keys_tuple):
    """Get a dictionary of which keys are class keys in string, and values are labels in integer.
    This includes the reversed duplicates, so two of the keys indicate one label value.
    exception: x during x == x during x so only one indicates one label.
    """

    class_keys_to_labels_dict = {}
    for i, class_key in enumerate(class_keys_tuple):
        class_key1, class_key2 = class_to_string(class_key, return_duplicate=True)
        class_keys_to_labels_dict[class_key1] = i
        class_keys_to_labels_dict[class_key2] = i

    return class_keys_to_labels_dict


def main():
    print(class_keys_task1())
    print(class_keys_task2())



if __name__ == '__main__':
    main()
