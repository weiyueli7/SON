import json
import numpy as np

CLASSES = {0: 'person',
 1: 'bicycle',
 2: 'car',
 3: 'motorcycle',
 4: 'airplane',
 5: 'bus',
 6: 'train',
 7: 'truck',
 8: 'boat',
 9: 'traffic light',
 10: 'fire hydrant',
 11: 'stop sign',
 12: 'parking meter',
 13: 'bench',
 14: 'bird',
 15: 'cat',
 16: 'dog',
 17: 'horse',
 18: 'sheep',
 19: 'cow',
 20: 'elephant',
 21: 'bear',
 22: 'zebra',
 23: 'giraffe',
 24: 'backpack',
 25: 'umbrella',
 26: 'handbag',
 27: 'tie',
 28: 'suitcase',
 29: 'frisbee',
 30: 'skis',
 31: 'snowboard',
 32: 'sports ball',
 33: 'kite',
 34: 'baseball bat',
 35: 'baseball glove',
 36: 'skateboard',
 37: 'surfboard',
 38: 'tennis racket',
 39: 'bottle',
 40: 'wine glass',
 41: 'cup',
 42: 'fork',
 43: 'knife',
 44: 'spoon',
 45: 'bowl',
 46: 'banana',
 47: 'apple',
 48: 'sandwich',
 49: 'orange',
 50: 'broccoli',
 51: 'carrot',
 52: 'hot dog',
 53: 'pizza',
 54: 'donut',
 55: 'cake',
 56: 'chair',
 57: 'couch',
 58: 'potted plant',
 59: 'bed',
 60: 'dining table',
 61: 'toilet',
 62: 'tv',
 63: 'laptop',
 64: 'mouse',
 65: 'remote',
 66: 'keyboard',
 67: 'cell phone',
 68: 'microwave',
 69: 'oven',
 70: 'toaster',
 71: 'sink',
 72: 'refrigerator',
 73: 'book',
 74: 'clock',
 75: 'vase',
 76: 'scissors',
 77: 'teddy bear',
 78: 'hair drier',
 79: 'toothbrush'}
CLASSES = set(CLASSES.values())

np.random.seed(0)
data = json.load(open("data/sample.json"))
all_spatial_rel_phrases = {'above', 'below', 'to the left of', 'to the right of'}


def sample_new_obj(data):
    all_attributes = set(data['obj_attributes'])
    to_sample = CLASSES - all_attributes
    return np.random.choice(list(to_sample),1)[0]

def add_more_objects(data_pt, num_new_objects):
    new_data_pt = {}
    new_data_pt['unique_id'] = data_pt['unique_id']
    new_data_pt['num_objects'] = int(data_pt['num_objects'] + num_new_objects)
    new_data_pt['obj_attributes'] = data_pt['obj_1_attributes'] + data_pt['obj_2_attributes']
    new_data_pt['rel_type'] = [data_pt['rel_type']]
    for _ in range(1, num_new_objects + 1):
        new_data_pt['obj_attributes'].append(sample_new_obj(new_data_pt))
        new_data_pt['rel_type'].append(np.random.choice(list(all_spatial_rel_phrases), 1)[0])
    text = ". ".join([f'a {new_data_pt["obj_attributes"][i]} {new_data_pt["rel_type"][i]} a {new_data_pt["obj_attributes"][i+1]}' for i in range(len(new_data_pt['obj_attributes']) - 1)])
    new_data_pt['text'] = text
    return new_data_pt


new_num_objects = np.random.randint(1, 4, 400)
new_data = []
for ind, data_pt in enumerate(data):
    ramdom_num = np.random.randint(1, 4)
    new_data.append(add_more_objects(data_pt, new_num_objects[ind]))
new_data
json.dump(new_data, open("data/new_sample.json", "w"), indent=2)
