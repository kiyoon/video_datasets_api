import json
import os
import numpy as np

object_shape_to_idx = {'spl': 0, 'sphere': 1, 'cube': 2, 'cone': 3, 'cylinder': 4}
object_size_to_idx = {'small': 0, 'medium': 1, 'large': 2}
object_colour_to_idx = {'red': 0, 'green': 1, 'blue': 2, 'cyan': 3, 'yellow': 4, 'purple': 5, 'brown': 6, 'gray': 7, 'gold': 8}
object_material_to_idx = {'metal': 0, 'rubber': 1}

NUM_FRAMES = 301

if __name__ == '__main__':
    scenes_path = '/home/kiyoon/datasets/cater/all_actions/scenes'
    #scenes_path = '/media/kiyoon/Elements1/datasets/CATER/max2actions/scenes'


    for root, dirs, files in os.walk(scenes_path):
        for filename in files:
            with open(os.path.join(root, filename), 'r') as f:
                scene = json.load(f)

            data = np.ones((NUM_FRAMES, 10, 7), dtype=np.float) * (-1)  # num_frames, num_objects, [material, size, shape, color, location_xyz]

            num_objects = len(scene['objects'])

            for objidx in range(num_objects):
                for frameidx in range(NUM_FRAMES):
                    data[frameidx, objidx, 0] = object_material_to_idx[scene['objects'][objidx]['material']]
                    data[frameidx, objidx, 1] = object_size_to_idx[scene['objects'][objidx]['size']]
                    data[frameidx, objidx, 2] = object_shape_to_idx[scene['objects'][objidx]['shape']]
                    data[frameidx, objidx, 3] = object_colour_to_idx[scene['objects'][objidx]['color']]
                    data[frameidx, objidx, 4:] = scene['objects'][objidx]['locations'][str(frameidx)]

#            print(data)


        

