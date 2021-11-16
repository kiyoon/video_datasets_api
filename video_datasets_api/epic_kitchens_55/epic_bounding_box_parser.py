
import csv


def EPIC_parse_object_bounding_box_labels(video_id, label_path, height_width_representation = True):

    output_dict = {}
    with open(label_path) as f:
        input_file = csv.DictReader(f)

        for row in input_file:
            if row['video_id'] == video_id:
                frame = int(row['frame'])
                if frame not in output_dict.keys():
                    output_dict[frame] = {'boxes': [], 'classes': []}

                bounding_boxes = eval(row['bounding_boxes'])
                for bounding_box in bounding_boxes:
                    if not height_width_representation:
                        # (ymin, xmin, height, width)
                        bounding_box = (bounding_box[0], bounding_box[1], bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3])
                    else:
                        # (ymin, xmin, ymax, xmax)
                        pass

                    output_dict[frame]['boxes'].append(bounding_box)
                    output_dict[frame]['classes'].append(int(row['noun_class']))

    return output_dict



if __name__ == '__main__':
    output_dict = EPIC_parse_object_bounding_box_labels('P01_01')
    print(output_dict)
