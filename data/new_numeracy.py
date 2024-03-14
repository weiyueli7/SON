import json
import numpy as np
from textblob import TextBlob

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





data = json.load(open('nsr-counting.json'))

types = set()
comparison = []
real = []
single_category = []
two_categories = []
for d in data:
    types.add(d['sub-type'])
    if d['sub-type'] == 'comparison':
        comparison.append(d)
    elif d['sub-type'] == 'real':
        real.append(d)
    elif d['sub-type'] == 'single-category':
        single_category.append(d)
    elif d['sub-type'] == 'two-categories':
        two_categories.append(d)

comparison.extend(single_category)
comparison.extend(two_categories)


templates = {
    "v1": "There are {}, {}, {}, and {} in the image.",
    "v2": "{} with {} and {} are in the photo.",
    "v3": "An image with {}, {}, and {} with {}.",
    "v4": "{} along with {} and {} are in the picture.",
    "v5": "{}, {}, and {}.",
    "v6": "{} together with {}, {}, and {}.",
    "v7": "A photo with {}, {}, and {} along with {}."
}
def get_plural(word):
    blobWord = TextBlob(word)
    return blobWord.words.pluralize()[0]

three_categories = ['v2', 'v4', 'v5']
four_categories = ['v1', 'v3', 'v6', 'v7']
num_conversion = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
}


indcies = np.random.choice(len(comparison), 200, replace=False)

new_data = []
for idx, d in enumerate(comparison):
    if idx not in indcies:
        continue
    new_d = {}
    new_d['id'] = int(idx)
    new_d['num_object'] = d['num_object']
    new_d['prompt'] = "A realistic scene: " + d['prompt']
    new_d['type'] = d['sub-type']
    new_data.append(new_d)



multi_category = []
for i in range(1, 201):
    cur_data = {}
    cur_data['id'] = 200 + i
    
    num_object = np.random.choice([3, 4])
    objects = np.random.choice(list(CLASSES), num_object, replace=False)
    num_objects = []
    for obj in objects:
        cur_num = int(np.random.choice([1, 2, 3]))
        num_objects.append([obj, cur_num])
    cur_data['num_object'] = num_objects
    formated_objects = []
    for obj, num in num_objects:
        if " " in obj:
            f, s = obj.split(" ")
            if num > 1:
                s = get_plural(s)
            else:
                s = s
            formated_objects.append(f"{num_conversion[num]} {f} {s}")
        else:
            if num > 1:
                obj = get_plural(obj)
            else:
                obj = obj
            formated_objects.append(f"{num_conversion[num]} {obj}")
    if num_object == 3:
        cur_prompt = templates[np.random.choice(three_categories)].format(*formated_objects)
        cur_prompt = cur_prompt[0].upper() + cur_prompt[1:]
        cur_data['prompt'] = "A realistic scene: " + cur_prompt
    else:
        cur_prompt = templates[np.random.choice(four_categories)].format(*formated_objects)
        cur_prompt = cur_prompt[0].upper() + cur_prompt[1:]
        cur_data['prompt'] = "A realistic scene: " + cur_prompt
    cur_data['type'] = f'{num_conversion[num_object]}-categories'
    multi_category.append(cur_data)

new_data.extend(multi_category)


json.dump(new_data, open('lmd_numeracy.json', 'w'), indent=2)