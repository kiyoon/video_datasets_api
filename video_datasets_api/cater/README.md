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
```

# Q&A
## Why 0 to 300?? 301 frames total?
It is because of the `num_frames + 1` in `random_objects_movements()` in `actions.py`.  
[actions.py#L40](https://github.com/rohitgirdhar/CATER/blob/13a19643f1a2fb24e931df25abd74353e4f2fdcb/generate/actions.py#L40)  
Looking at `add_movements_singleObj()` and `add_movements_multiObj_try()`,  
`end_frame` can be `total_frames=300`, which means there are actually `total_frames+1=301` frames.

The paper says: "we render 300-frame 320x240px videos", but it is obviously wrong.

## How start/end frames of movements are defined.
According to the paper, "We split the video into 30-frame slots, and each action is contained within these slots".  
and "For each action, we pick a random start and end time from within the 30-frame slot."  

This is confusing because it sounds like there are 10 time slots throughout a video, and the actions should be defined within 0-29, 30-59, 60-89, ... frames.  
However, you see that the start and end time of the movements don't follow the rule.

In fact, the duration of the time slots is 20-40 frames chosen randomly, (explanation below)  
and the new time slot starts one frame after the last time slot ends.
```python
cur_frame = end_frame + 1
```
[actions.py#L58](https://github.com/rohitgirdhar/CATER/blob/13a19643f1a2fb24e931df25abd74353e4f2fdcb/generate/actions.py#L58)  
The time slot ends at the frame that every motion ends.  
(`add_movements_singleObj()` returns `last_frame_added` which is `max(new_end_frame, last_frame_added)` and  
`add_movements_multiObj_try()` returns `max(new_end_frame, new_end_frame_singleObjMotion)`)

In each time slot, start the motion at timeslot_start+random.randint(0,10).  
That means 0 to 10 frames of delay in the movement.  

The duration of the movement is `random.randint(MOVEMENT_MIN, MOVEMENT_MAX)`, that is, 20-30 frames, since  
```python
MOVEMENT_MIN = 20
MOVEMENT_MAX = 30
```
[actions.py#L87](https://github.com/rohitgirdhar/CATER/blob/13a19643f1a2fb24e931df25abd74353e4f2fdcb/generate/actions.py#L87)  

Therefore, the duration of the time slot is from 20 to 40. (`0 + 20 = 20` to `10 + 30 = 40`)  

There is no time slot starting from frame > 270, because of 
```python
while cur_frame <= total_frames - MOVEMENT_MAX:
```
[actions.py#L52-L58](https://github.com/rohitgirdhar/CATER/blob/13a19643f1a2fb24e931df25abd74353e4f2fdcb/generate/actions.py#L52-L58)


The scenes file does not have any time slot information. Use `get_time_slots()` in `generate_labels_from_scenes.py` in this repo, to get the time slot information.

## In each time slot, how are the motion selected?

They choose `add_movements_singleObj()` or `add_movements_multiObj_try()` randomly (50/50 chance).  
The former is for non-containment, and the latter is for containment.  
The latter can also fail after 100 tries and you have another 50/50 chance of calling either of the two functions.  
Apparently, the latter fails quite frequently, because containment does not happen as frequent as other actions.

If `add_movements_multiObj_try(max_motions=K)` is succeeded, call `add_movements_singleObj(max_motions=K-1)`.  
This means that there will be no two containments happening in the same time slot.

## What about the Cameramotion?

`add_random_camera_motion()` in `render_videos.py`, it's always 30-frame interval with 10 random points.  
That is, the camera positions are defined in `[30, 60, 90, 120, 150, 180, 210, 240, 270, 300]` and it starts from the same position at frame 0.  
[render_videos.py#L565-L574](https://github.com/rohitgirdhar/CATER/blob/13a19643f1a2fb24e931df25abd74353e4f2fdcb/generate/render_videos.py#L565-L574)

Unfortunately, the scenes does not have any camera position information. You can indirectly infer from the movements start and end frame.

## Task2 - Ordering
According to `get_ordering` from [gen_train_test.py#L100](https://github.com/rohitgirdhar/CATER/blob/13a19643f1a2fb24e931df25abd74353e4f2fdcb/generate/gen_train_test.py#L100), when the start and end time is the same with two primitive actions (edge cases), they're defined as `before` and `after` rather than `during`.
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

## Slide of the contained object - is it annotated in scenes?
Yes, however, they have no additional flag indicating whether it is contained. It has to be inferred by back-tracking containment.

## Why is generating task2 dataset in original CATER repo so slow?
[`actions_order_dataset()` in `gen_train_test.py`](https://github.com/rohitgirdhar/CATER/blob/13a19643f1a2fb24e931df25abd74353e4f2fdcb/generate/gen_train_test.py#L169) generates the task2 dataset, and  
[`compute_active_labels()` in `gen_train_test.py`](https://github.com/rohitgirdhar/CATER/blob/13a19643f1a2fb24e931df25abd74353e4f2fdcb/generate/gen_train_test.py#L131) generates the label for each video.  
However, the code is really poorly implemented, so you'd better use my code `generate_task2_labels_from_scenes()` in `generate_labels_from_scenes.py`.

On my laptop, it takes **304.0 seconds** to generate the whole dataset labels with the CATER code, and **1.2 seconds** with mine. Nearly 300 times faster.  
I made sure that my function generates exactly the same labels as the original one.

## There are broken videos in the dataset?
Yes, there are some broken videos in the dataset.  
[`check_avi_broken()` in `gen_train_test.py`](https://github.com/rohitgirdhar/CATER/blob/13a19643f1a2fb24e931df25abd74353e4f2fdcb/generate/gen_train_test.py#L209) checks broken video files, but **some videos are not generated fully or broken.**

You have to extract the videos into frames, and check if they have frame 0 to frame 300, totalling 301 image files.  
Or, you can use the provided corrupted video ids from this repository.

```python
from video_datasets_api.cater.definitions import CORRUPTED_VIDEO_IDS_MAX2ACTION
```
