# scenes



```python
>>> scene = json.load(f)
>>> scene.keys()
dict_keys(['movements', 'directions', 'image_filename', 'split', 'objects', 'relationships', 'image_index'])

>>> scene['movements']
{'Cone_0': [['_slide', None, 5, 31], ['_pick_place', None, 48, 77], ['_pick_place', None, 81, 106], ['_pick_place', None, 120, 148], ['_contain', 'Spl_0', 164, 186], ['_pick_place', None, 197, 225], ['_slide', None, 243, 263]], 'SmoothCylinder-Short_0': [['_rotate', None, 8, 38], ['_rotate', None, 47, 77], ['_rotate', None, 82, 107], ['_rotate', None, 124, 153], ['_pick_place', None, 158, 179], ['_rotate', None, 202, 224], [[-0.8938594460487366, -1.9115666151046753, 0.3421497941017151]'_rotate', None, 239, 266]], 'SmoothCube_v2_1': [['_rotate', None, 7, 32], ['_rotate', None, 42, 65], ['_rotate', None, 78, 108], ['_rotate', None, 121, 141], ['_rotate', None, 166, 186], ['_rotate', None, 207, 231], ['_rotate', None, 242, 270]], 'SmoothCylinder-Short_2': [['_rotate', None, 0, 25], ['_rotate', None, 39, 62], ['_pick_place', None, 86, 114], ['_pick_place', None, 126, 155], ['_slide', None, 158, 185], ['_rotate', None, 202, 223], ['_rotate', None, 245, 269]], 'Cone_1': [['_slide', None, 10, 35], ['_slide', None, 43, 66], ['_slide', None, 83, 104], ['_slide', None, 125, 149], ['_pick_place', None, 157, 187], ['_pick_place', None, 206, 231], ['_slide', None, 241, 268]], 'Spl_0': [['_rotate', None, 6, 34], ['_slide', None, 40, 65], ['_rotate', None, 78, 99], ['_rotate', None, 129, 156], ['_no_op', None, 197, 225], ['_rotate', None, 247, 269]], 'SmoothCylinder-Short_1': [['_rotate', None, 3, 23], ['_rotate', None, 40, 60], ['_rotate', None, 85, 115], ['_rotate', None, 120, 147], ['_rotate', None, 166, 196], ['_rotate', None, 202, 231], ['_pick_place', None, 239, 266]], 'SmoothCube_v2_0': [['_rotate', None, 3, 30], ['_rotate', None, 45, 69], ['_pick_place', None, 88, 118], ['_rotate', None, 120, 145], ['_rotate', None, 157, 184], ['_pick_place', None, 206, 235], ['_rotate', None, 248, 268]], 'SmoothCube_v2_2': [['_pick_place', None, 6, 26], ['_rotate', None, 45, 74], ['_rotate', None, 79, 107], ['_rotate', None, 122, 143], ['_rotate', None, 165, 189], ['_pick_place', None, 204, 227], ['_rotate', None, 243, 267]], 'Sphere_0': [['_slide', None, 8, 28], ['_slide', None, 43, 68], ['_slide', None, 79, 107], ['_pick_place', None, 128, 149], ['_slide', None, 160, 188], ['_pick_place', None, 207, 237], ['_slide', None, 243, 273]]}
# [0] movement: _slide, _rotate, _pick_place, _contain, _no_op
# _no_op is called when the objects are splitting from being contained.
# The top object is _pick_place and the bottom rests (can be 1 or more) are _no_op
# refer to https://github.com/rohitgirdhar/CATER/blob/master/generate/actions.py
# [1]: if _contain, the object being contained.
# [2]: Start frame: 0~300
# [3]: End frame: 0~300

>>> scene['directions']
{'right': [0.6571769714355469, 0.7537363767623901, -0.0], 'behind': [-0.7537363171577454, 0.6571769714355469, 0.0], 'below': [-0.0, -0.0, -1.0], 'left': [-0.6571769714355469, -0.7537363767623901, 0.0], 'front': [0.7537363171577454, -0.6571769714355469, -0.0], 'above': [0.0, 0.0, 1.0]}

>>> scene['split']
new
# ????

>>> scene['relationships']
{'right': [[1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 8], [1, 2, 3, 4, 5, 6, 8, 9], [], [], [], [], [5], [5], [5], [5], [5], [], [1], [1], [1, 4], [1, 4, 5], [1, 4, 5], [1, 4, 5], [1, 4, 5, 8], [1, 4, 5, 8, 9], [], [1], [1, 2], [1, 2, 4], [1, 2, 4, 5], [1, 2, 4, 5], [1, 2, 4, 5], [1, 2, 4, 5, 8], [1, 2, 4, 5, 8, 9], [], [1], [1], [1], [1, 5], [1, 5], [1, 5], [1, 5, 8], [1, 5, 8, 9], [], [], [], [], [], [], [], [], [], [], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 8], [1, 2, 3, 4, 5, 8, 9], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6, 8], [0, 1, 2, 3, 4, 5, 6, 8, 9], [], [1], [1], [1], [1], [1, 5], [1, 5], [1, 5], [1, 5], [], [1], [1], [1], [1], [1, 5], [1, 5], [1, 5], [1, 5, 8]], 'behind': [[1], [1], [1], [1, 4], [1, 4], [1, 4, 6], [1, 4, 6], [1, 4, 6], [1, 4, 6], [], [], [], [4], [4], [4, 6], [4, 6], [4, 6], [4, 6], [0], [0, 1], [0, 1, 3], [0, 1, 3, 4], [0, 1, 3, 4, 5], [0, 1, 3, 4, 5, 6], [0, 1, 3, 4, 5, 6, 7], [0, 1, 3, 4, 5, 6, 7, 8], [0, 1, 3, 4, 5, 6, 7, 8, 9], [0], [0, 1], [0, 1], [0, 1, 4], [0, 1, 4, 5], [0, 1, 4, 5, 6], [0, 1, 4, 5, 6, 7], [0, 1, 4, 5, 6, 7], [0, 1, 4, 5, 6, 7, 9], [], [], [], [], [], [], [], [], [], [0], [0, 1], [0, 1], [0, 1], [0, 1, 4], [0, 1, 4, 6], [0, 1, 4, 6], [0, 1, 4, 6], [0, 1, 4, 6], [], [], [], [], [4], [4], [4], [4], [4], [0], [0, 1], [0, 1], [0, 1], [0, 1, 4], [0, 1, 4, 5], [0, 1, 4, 5, 6], [0, 1, 4, 5, 6], [0, 1, 4, 5, 6], [0], [0, 1], [0, 1], [0, 1, 3], [0, 1, 3, 4], [0, 1, 3, 4, 5], [0, 1, 3, 4, 5, 6], [0, 1, 3, 4, 5, 6, 7], [0, 1, 3, 4, 5, 6, 7, 9], [0], [0, 1], [0, 1], [0, 1], [0, 1, 4], [0, 1, 4, 5], [0, 1, 4, 5, 6], [0, 1, 4, 5, 6, 7], [0, 1, 4, 5, 6, 7]], 'left': [[], [], [], [], [], [], [7], [7], [7], [0], [0, 2], [0, 2, 3], [0, 2, 3, 4], [0, 2, 3, 4], [0, 2, 3, 4, 6], [0, 2, 3, 4, 6, 7], [0, 2, 3, 4, 6, 7, 8], [0, 2, 3, 4, 6, 7, 8, 9], [0], [0], [0, 3], [0, 3], [0, 3], [0, 3, 6], [0, 3, 6, 7], [0, 3, 6, 7], [0, 3, 6, 7], [0], [0], [0], [0], [0], [0, 6], [0, 6, 7], [0, 6, 7], [0, 6, [-0.8938594460487366, -1.9115666151046753, 0.3421497941017151]7], [0], [0], [0, 2], [0, 2, 3], [0, 2, 3], [0, 2, 3, 6], [0, 2, 3, 6, 7], [0, 2, 3, 6, 7], [0, 2, 3, 6, 7], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 6], [0, 1, 2, 3, 4, 6, 7], [0, 1, 2, 3, 4, 6, 7, 8], [0, 1, 2, 3, 4, 6, 7, 8, 9], [0], [0], [0], [0], [0], [0], [0, 7], [0, 7], [0, 7], [], [], [], [], [], [], [], [], [], [0], [0], [0, 2], [0, 2, 3], [0, 2, 3, 4], [0, 2, 3, 4], [0, 2, 3, 4, 6], [0, 2, 3, 4, 6, 7], [0, 2, 3, 4, 6, 7, 9], [0], [0], [0, 2], [0, 2, 3], [0, 2, 3, 4], [0, 2, 3, 4], [0, 2, 3, 4, 6], [0, 2, 3, 4, 6, 7], [0, 2, 3, 4, 6, 7]], 'front': [[], [2], [2, 3], [2, 3], [2, 3, 5], [2, 3, 5], [2, 3, 5, 7], [2, 3, 5, 7, 8], [2, 3, 5, 7, 8, 9], [0], [0, 2], [0, 2, 3], [0, 2, 3], [0, 2, 3, 5], [0, 2, 3, 5], [0, 2, 3, 5, 7], [0, 2, 3, 5, 7, 8], [0, 2, 3, 5, 7, 8, 9], [], [], [], [], [], [], [], [], [], [], [], [2], [2], [2], [2], [2], [2, 8], [2, 8], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 5], [0, 1, 2, 3, 5, 6], [0, 1, 2, 3, 5, 6, 7], [0, 1, 2, 3, 5, 6, 7, 8], [0, 1, 2, 3, 5, 6, 7, 8, 9], [], [], [2], [2, 3], [2, 3], [2, 3], [2, 3, 7], [2, 3, 7, 8], [2, 3, 7, 8, 9], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3, 5], [0, 1, 2, 3, 5, 7], [0, 1, 2, 3, 5, 7, 8], [0, 1, 2, 3, 5, 7, 8, 9], [], [], [2], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3, 8], [2, 3, 8, 9], [], [], [2], [2], [2], [2], [2], [2], [2], [], [], [2], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3, 8]]}
# ????

>>> scene['image_filename']
CLEVR_new_000002.avi

>>> scene['image_index']
2
```

## scene['objects']

```python
>>> len(scene['objects'])
10
# minimum: 5, maximum: 10

>>> scene['objects'][0].keys()
dict_keys(['3d_coords', 'material', 'instance', 'pixel_coords', 'size', 'rotation', 'shape', 'color', 'locations', 'sized'])

>>> scene['objects'][0]['3d_coords']
[-2.6014318466186523, -1.5313814878463745, 0.3421497941017151]

>>> scene['objects'][0]['material']
metal
# metal or rubber

>>> scene['objects'][0]['instance']
Spl_0

# Spl, Sphere, SmoothCylinder-Short, SmoothCube_v2, Cone

>>> scene['objects'][0]['pixel_coords']
[72, 97, 11.4039888381958]

>>> scene['objects'][0]['size']
small
# small, medium, large

>>> scene['objects'][0]['rotation']
102.59546083799643

>>> scene['objects'][0]['shape']
spl
# spl, sphere, cube, cone, cylinder
# object '0' is always snitch (spl) which is the object of interest

>>> scene['objects'][0]['color']
gold
# red, green, blue, cyan, yellow, purple, brown, gray, gold

>>> scene['objects'][0]['sized']
0.3
```

### scene['objects'][0]['locations']

```python
>>> scene['objects'][0]['locations']['0']
[-2.6014318466186523, -1.5313814878463745, 0.3421497941017151]

>>> scene['objects'][0]['locations']['300']
[-0.8938594460487366, -1.9115666151046753, 0.3421497941017151]

# Why 0 to 300?? 301 frames total?
```

# Task2:
## Ordering
According to `get_ordering` from [this code](https://github.com/rohitgirdhar/CATER/blob/13a19643f1a2fb24e931df25abd74353e4f2fdcb/generate/gen_train_test.py#L100), when the start and end time is the same with two primitive actions (edge cases), they're defined as `before` and `after` rather than `during`.
```python
def get_ordering(act1_time, act2_time):
    if act1_time[1] <= act2_time[0]:
        # act1 should finish before act2 starts
        return _BEFORE
    elif act2_time[1] <= act1_time[0]:
        # act1 should start after act2 ends
        return _AFTER
    else:
        # We define everything else as "during", though it might be partly
        # overlapped etc
        return _DURING
```
