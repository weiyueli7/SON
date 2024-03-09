from ultralytics import YOLO
import os
import numpy as np
import time
import json
import argparse
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from tqdm import tqdm
import re


img_width, img_height = 512, 512

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# cur_time = time.strftime("%I:%M%pon%B%d,%Y")

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

def detecting_objects(DIR):
    print(f"Loading model ({YOLO_MODEL}.pt)...")
    model = YOLO(f"{YOLO_MODEL}.pt")
    # DIR = f"img_generations/img_generations_templatev0.3_lmd_plus_demo_gpt-4/run0"
    # print(os.listdir(DIR))
    for dir in os.listdir(DIR):
        if os.path.isdir(os.path.join(DIR, dir)):
            for file in os.listdir(os.path.join(DIR, dir)):
                if file.endswith("0.png"):
                    cur_path = os.path.join(DIR, dir, file)
                    results = model.predict(
                        os.path.join(DIR, dir, file), 
                        save=True, 
                        imgsz=512, 
                        save_txt=True, 
                        project=f"object_detection/{YOLO_MODEL}/{DIR[16:]}", 
                        name=f"results_{dir}"
                        )


def convert_center_to_corner(bbox, img_width, img_height):
    """
    Convert YOLO format (center x, center y, width, height) to corner format
    (top-left x, top-left y, width, height).
    """
    cx, cy, w, h = bbox
    tl_x = (cx - w / 2) * img_width
    tl_y = (cy - h / 2) * img_height
    width = w * img_width
    height = h * img_height
    return [tl_x, tl_y, width, height]

def convert_corner_to_center(bbox, img_width, img_height):
    """
    Convert bounding box in corner format (top-left x, top-left y, width, height) to
    YOLO format (center x, center y, width, height).
    """
    tl_x, tl_y, width, height = bbox
    cx = (tl_x + width / 2) / img_width
    cy = (tl_y + height / 2) / img_height
    w = width / img_width
    h = height / img_height
    return [cx, cy, w, h]

def calculate_iou(boxA, boxB):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    """
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)

    boxAArea = boxA[2] * boxA[3]
    boxBArea = boxB[2] * boxB[3]

    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou


def find_key_for_value(my_dict, search_value):
    """
    Finds the first key in the dictionary that corresponds to the given value.
    
    Parameters:
    my_dict (dict): The dictionary to search through.
    search_value: The value for which the corresponding key is to be found.

    Returns:
    The key corresponding to the given value if found, otherwise None.
    """
    for key, value in my_dict.items():
        if search_value in value:
            return key
    return None

def euclidean_distance(point1, point2):

    x1, y1 = point1
    x2, y2 = point2
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def numeracy_eval(objects, text_objects):
    print(objects)
    print("------")
    print(text_objects)
    groud_truth = [obj[1] for obj in text_objects['num_object']]
    print("groud truth", groud_truth)
    objects_keys = [re.sub(r'\s*\d+', '', obj[0]) for obj in objects]
    objects_keys = [obj[2:] if obj.startswith("a ") else obj[3:] if obj.startswith("an ") else obj for obj in objects_keys]
    print("object keys", objects_keys)
    prediction = [objects_keys.count(obj[0]) for obj in text_objects['num_object']]
    print(prediction)
    if text_objects['type'] == 'comparison':
        obj1, obj2 = text_objects['num_object']
        rel = []
        if obj1[1] > obj2[1]:
            rel += "more"
        elif obj1[1] < obj2[1]:
            rel += "less"
        else:
            rel += "equal"
        prd_rel = []
        if prediction[0] > prediction[1]:
            prd_rel += "more"
        elif prediction[0] < prediction[1]:
            prd_rel += "less"
        else:
            prd_rel += "equal"
        if rel == prd_rel:
            return 0, 0, 1
        else:
            return 0, 0, 0

    prediction = [objects_keys.count(obj[0]) for obj in text_objects['num_object']]
    print(groud_truth)
    print(prediction)
    try:
        precision = sum([min(groud_truth[i], prediction[i]) for i in range(len(groud_truth))])/sum(prediction)
    except:
        precision = 0
    try:
        recall = sum([min(groud_truth[i], prediction[i]) for i in range(len(groud_truth))])/sum(groud_truth)
    except:
        recall = 0

    return precision, recall, prediction == groud_truth

def spatial_eval(ind, converted_detections):
    annotation = GROUND_TRUTH[ind]
    # print(annotation)
    print(converted_detections)
    obj_attributes = annotation['obj_attributes']
    converted_detections_objects = [det[0] for det in converted_detections]

    centroid = [[rect[1][0]+rect[1][2]//2, rect[1][1]+rect[1][3]//2] for rect in converted_detections]

    credit = 0
    credit_2 = 0
    for idx in range(len(obj_attributes) - 1):
        if obj_attributes[idx] not in converted_detections_objects or obj_attributes[idx + 1] not in converted_detections_objects:
            continue
        locate_idx1_choices = [i for i in range(len(converted_detections_objects)) if converted_detections_objects[i] == obj_attributes[idx]]#converted_detections_objects.index(obj_attributes[idx])
        locate_idx2_choices = [i for i in range(len(converted_detections_objects)) if converted_detections_objects[i] == obj_attributes[idx+1]]#converted_detections_objects.index(obj_attributes[idx + 1])
        # print(locate_idx1, locate_idx2)
        relationship = []
        for locate_idx1 in locate_idx1_choices:
            for locate_idx2 in locate_idx2_choices:
                cur_rel = []
                d = euclidean_distance(centroid[locate_idx1], centroid[locate_idx2])
                if (centroid[locate_idx2][1] - centroid[locate_idx1][1])/d >= np.sin(np.pi/4):
                    cur_rel += ["above"]
                if (centroid[locate_idx2][1] - centroid[locate_idx1][1])/d <= np.sin(-np.pi/4):
                    cur_rel += ["below"]
                if (centroid[locate_idx1][0] - centroid[locate_idx2][0])/d >= np.cos(np.pi/4):
                    cur_rel += ["to the right of"]
                if (centroid[locate_idx1][0] - centroid[locate_idx2][0])/d <= np.cos(3*np.pi/4):
                    cur_rel += ["to the left of"]
                # print(relationship)
                box1, box2 = converted_detections[locate_idx1][1], converted_detections[locate_idx2][1]
                iou = calculate_iou(box1, box2)
                cur_rel.append(iou)
                relationship.append(cur_rel)

        for rel in relationship:
            if annotation['rel_type'][idx] in rel:
                credit += 1
                if rel[-1] < 0.1:
                    credit_2 += 1
                break


    return credit/len(annotation['rel_type']), credit_2/len(annotation['rel_type'])

def decode_yolo_output(yolo_file_path):
    yolo_detections = []

    # Read the file and parse the data
    with open(yolo_file_path, 'r') as file:
        for line in file:
            # Split the line into components and convert them to the correct data type
            class_id, cx, cy, w, h = line.strip().split()
            class_id = int(class_id)
            cx, cy, w, h = map(float, [cx, cy, w, h])

            # Append the parsed data to yolo_detections
            yolo_detections.append((class_id, cx, cy, w, h))
    return yolo_detections


def get_converted_detections(yolo_detections, target_objs):
    converted_detections = []
    all_detected_objects = set()
    for det in yolo_detections:
        # print(det)
        class_id = CLASSES[det[0]]
        all_detected_objects.add(class_id)
        
        if class_id in target_objs:
            bbox = convert_center_to_corner(det[1:], img_width, img_height)
            converted_detections.append([class_id, bbox])
    return converted_detections, all_detected_objects

def evaluate_image(yolo_file_path, original_prompt, ind):

    yolo_detections = decode_yolo_output(yolo_file_path)
    print("yolo_detections", yolo_detections)

    if args.task == 'numeracy':
        target_objs = [i[0] for i in GROUND_TRUTH[ind]['num_object']]
    else:
        target_objs = set(GROUND_TRUTH[ind]['obj_attributes'])
    # print("target objects", target_objs)
    converted_detections, all_detected_objects = get_converted_detections(yolo_detections, target_objs)
    # print("converted_detections", converted_detections)

    expected_count = len(target_objs)
    detected_count = len(converted_detections)
    count_accuracy = abs(detected_count - expected_count) / expected_count

    # Evaluate Bounding Box Accuracy
    # iou_threshold = 0.9
    all_ious = []
    # uni_det = []
    # accurate_boxes = 0
    for class_id, det_box in converted_detections:
        # print(det_box)
        cur_ious = []
        for _, org_box in original_prompt:
            iou = calculate_iou(det_box, org_box)
            cur_ious.append(iou)
        # print(cur_ious)
        all_ious.append(max(cur_ious))

    class_id_to_name = CLASSES
    expected_objects = target_objs 
    extra_detected_objects = all_detected_objects.difference(expected_objects)

    print(extra_detected_objects)
    # extra_detected_objects_names = [class_id_to_name[obj_id] for obj_id in extra_detected_objects]

    print(target_objs)
    print(converted_detections)
    ious_between_detections = []
    for i in range(len(converted_detections)):
        for j in range(i + 1, len(converted_detections)):
            iou = calculate_iou(converted_detections[i][1], converted_detections[j][1])
            ious_between_detections.append(iou)
    

    spatial_acc = 0
    if 'spatial' in args.prompt_type:
        spatial_acc, uni_det = spatial_eval(ind, converted_detections)
    if 'numeracy' in args.prompt_type:
        text_objects = GROUND_TRUTH[ind]
        precision, recall, num_acc = numeracy_eval(converted_detections, text_objects)

    if all_ious == []:
        all_ious = [0]
    if ious_between_detections == []:
        ious_between_detections = [0]
    # Results
    if args.task == 'spatial':
        return count_accuracy, np.mean(all_ious), extra_detected_objects, spatial_acc, uni_det, np.mean(ious_between_detections)
    elif args.task == 'complex':

        return count_accuracy, np.mean(all_ious), np.mean(ious_between_detections)
    else:
        return count_accuracy, np.mean(all_ious), np.mean(ious_between_detections), precision, recall, num_acc
    return count_accuracy, np.mean(all_ious), extra_detected_objects, spatial_acc, uni_det



def extract_noun(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Part-of-speech tagging
    tagged = pos_tag(tokens)
    # Extract nouns
    nouns = [word for word, pos in tagged if pos.startswith('NN')]
    return nouns[0]

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--lm", default='gpt-4', type=str)
    parser.add_argument("--template_version", default='v0.1', type=str)
    parser.add_argument("--prompt_type", default='lmd_spatial', type=str, help="lmd_xxx or raw")
    parser.add_argument("--sdxl", default=True, type=bool)
    parser.add_argument("--model_type", default='lmd', type=str, help="The model type to evaluate. (lmd, sdxl, tokencompose, etc.)")
    parser.add_argument("--task", default='spatial', type=str)
    parser.add_argument("--yolo_model", default='yolov8m', type=str, help="The YOLO model to use for object detection. (yolov8m, yolov8x, yolov9e)")
    parser.add_argument("--detection", default=False, type=bool)
    args = parser.parse_args()


    YOLO_MODEL = args.yolo_model
    if args.model_type == 'lmd':
        if args.sdxl == True:
            DIR = f"img_generations/img_generations_template{args.template_version}_lmd_plus_{args.prompt_type}_{args.lm}_sdxl_0.3/run0"
        else:
            print("hi")
            DIR = f"img_generations/img_generations_template{args.template_version}_gligen_{args.prompt_type}_{args.lm}/run0"
    else:
        DIR = f"img_generations/{args.task}_{args.model_type}"
    # Detecting objects from synthetic images
    
    if args.detection == True:
        detecting_objects(DIR)


    # Evaluate the detected objects
    if args.prompt_type.startswith("lmd"):
        if args.lm == "gpt-3.5":
            prompts = json.load(open(f"cache/cache_{args.prompt_type.replace('lmd_', '')}_{args.template_version}_{args.lm}-turbo.json"))
        else:
            prompts = json.load(open(f"cache/cache_{args.prompt_type.replace('lmd_', '')}_{args.template_version}_{args.lm}.json"))
    else:
        prompts = json.load(open(f"cache/cache_demo_{args.template_version}_{args.lm}.json")) 
    if "spatial" in args.prompt_type:
        GROUND_TRUTH = json.load(open("data/new_sample_3.json"))
        if args.prompt_type == "raw":
            prompts = [d['text'] for d in GROUND_TRUTH]
    elif "numeracy" in args.prompt_type:
        GROUND_TRUTH = json.load(open("data/numeracy.json"))
    elif "complex" in args.prompt_type:
        GROUND_TRUTH = json.load(open("data/complex_prompt.json"))

    extra_miss_ratio = []
    ious = []
    spatial_accs = []
    uni_dets = []
    ious_stage2 = []
    precisions = []
    recalls = []
    num_accs = []

    if args.model_type == 'lmd':

        for ind, (key, value) in tqdm(enumerate(prompts.items())):
            original_prompt = eval(value[0].split("Background prompt:")[0])
            yolo_path = f"object_detection/{YOLO_MODEL}/{DIR[16:]}/results_{ind}/labels/img_0.txt"
            # eval_result = evaluate_image(yolo_path, original_prompt, ind)
            try:
                print("=================================")

                
                if args.task == 'spatial':
                    eval_result = evaluate_image(yolo_path, original_prompt, ind)
                    print(f"extra/miss ratio: {eval_result[0]}, mean_iou: {eval_result[1]}, extra_detected_objects: {eval_result[2]}, spatial accuracy: {eval_result[3]}, UniDet: {eval_result[4]}, mean_iou_stage2: {eval_result[5]}")
                    spatial_accs.append(eval_result[3])
                    uni_dets.append(eval_result[4])
                    extra_miss_ratio.append(eval_result[0])
                    ious.append(eval_result[1])
                if args.task == 'numeracy':
                    # print(1)
                    eval_result = evaluate_image(yolo_path, original_prompt, ind)

                    # numeracy_eval(ind, objects, text_objects)
                    print(f"extra/miss ratio: {eval_result[0]}, mean_iou: {eval_result[1]}, mean_iou_stage2: {eval_result[2]}, precision: {eval_result[3]}, recall: {eval_result[4]}, num_acc: {eval_result[5]}")
                    extra_miss_ratio.append(eval_result[0])
                    ious.append(eval_result[1])
                    ious_stage2.append(eval_result[2])
                    precisions.append(eval_result[3])
                    recalls.append(eval_result[4])
                    num_accs.append(eval_result[5])

                if args.task == 'complex':
                    eval_result = evaluate_image(yolo_path, original_prompt, ind)
                    print(f"extra/miss ratio: {eval_result[0]}, mean_iou(stage 1 vs 2): {eval_result[1]}, mean_iou(between stage2 objects): {eval_result[2]}")
                    extra_miss_ratio.append(eval_result[0])
                    ious.append(eval_result[1])
                    ious_stage2.append(eval_result[2])
                print("=================================")
                
            except:
                extra_miss_ratio.append(0)
                ious.append(0)
                spatial_accs.append(0)
                uni_dets.append(0)
                ious_stage2.append(0)
                precisions.append(0)
                recalls.append(0)
                num_accs.append(0)
                pass
            # if ind == 3:
            # break

        if args.task == 'spatial':
            print(f"Spatial Accuracy: {np.mean(spatial_accs)}")
            print(f"UniDet: {np.mean(uni_dets)}")
            print(f"Extra/Miss Ratio: {np.mean(extra_miss_ratio)}")
            print(f"Mean IoU: {np.mean(ious)}")
            eval_result = {
                "extra_miss_ratio": np.mean(extra_miss_ratio),
                "mean_iou": np.mean(ious),
                "UniDet": np.mean(uni_dets)
            }
        if args.task == 'complex':
            print(f"Extra/Miss Ratio: {np.mean(extra_miss_ratio)}")
            print(f"Mean IoU (stage 1 vs 2): {np.mean(ious)}")
            print(f"Mean IoU (between stage2 objects): {np.mean(ious_stage2)}")
            eval_result = {
                "extra_miss_ratio": np.mean(extra_miss_ratio),
                "mean_iou_stage1_2": np.mean(ious),
                "mean_iou_stage2": np.mean(ious_stage2)
            }
        if args.task == 'numeracy':
            print(f"Extra/Miss Ratio: {np.mean(extra_miss_ratio)}")
            print(f"Mean IoU: {np.mean(ious)}")
            print(f"Mean IoU (stage 2): {np.mean(ious_stage2)}")
            print(f"Precision: {np.mean(precisions)}")
            print(f"Recall: {np.mean(recalls)}")
            print(f"Numeracy Accuracy: {np.mean(num_accs)}")
            eval_result = {
                "extra_miss_ratio": np.mean(extra_miss_ratio),
                "mean_iou": np.mean(ious),
                "mean_iou_stage2": np.mean(ious_stage2),
                "precision": np.mean(precisions),
                "recall": np.mean(recalls),
                "numeracy_accuracy": np.mean(num_accs)
            }

        json.dump(eval_result, open(f"results/{YOLO_MODEL}_evaluation_result_{DIR[16:-5]}.json", "w"), indent=2)
    else:
        for ind, prompt in enumerate(prompts):

            yolo_path = f"object_detection/{YOLO_MODEL}/{DIR[16:]}/results_{ind}/labels/img_0.txt"

            try:
                
                yolo_detections = decode_yolo_output(yolo_path)
                try:
                    target_objs = set(GROUND_TRUTH[ind]['obj_attributes'])
                except:
                    target_objs = [i[0] for i in GROUND_TRUTH[ind]['num_object']]
                converted_detections, all_detected_objects = get_converted_detections(yolo_detections, target_objs)
                # print(1)
                if args.task == 'spatial':
                    spatial_acc, uni_det = spatial_eval(ind, converted_detections)
                    spatial_accs.append(spatial_acc)
                    uni_dets.append(uni_det)
                if args.task == 'numeracy':
                    # print(1)
                    text_objects = GROUND_TRUTH[ind]
                    precision, recall, num_acc = numeracy_eval(converted_detections, text_objects)
                    precisions.append(precision)
                    recalls.append(recall)
                    num_accs.append(num_acc)

                if args.task == 'complex':
                    pass
                ious_between_detections = []
                for i in range(len(converted_detections)):
                    for j in range(i + 1, len(converted_detections)):
                        iou = calculate_iou(converted_detections[i][1], converted_detections[j][1])
                        ious_between_detections.append(iou)
                if ious_between_detections == []:
                    ious_between_detections = [0]
                ious_stage2.append(np.mean(ious_between_detections))
                expected_count = len(target_objs)
                detected_count = len(converted_detections)
                count_accuracy = abs(detected_count - expected_count) / expected_count
                extra_miss_ratio.append(count_accuracy)


            except:
                extra_miss_ratio.append(0)
                spatial_accs.append(0)
                uni_dets.append(0)
                ious_stage2.append(0)
                precisions.append(0)
                recalls.append(0)
                num_accs.append(0)

                pass
            # if ind == 3:

            #     break
        if args.task == 'spatial':
            print(f"Extra/Miss Ratio: {np.mean(extra_miss_ratio)}")
            print(f"Spatial Accuracy: {np.mean(spatial_accs)}")
            print(f"UniDet: {np.mean(uni_dets)}")
            print(f"Mean IoU (between stage2 objects): {np.mean(ious_stage2)}")
            eval_result = {
                "extra_miss_ratio": np.mean(extra_miss_ratio),
                "spatial_accuracy": np.mean(spatial_accs),
                "UniDet": np.mean(uni_dets),
                "mean_iou_stage2": np.mean(ious_stage2)
        
            }
        if args.task == 'complex':
            print(f"Extra/Miss Ratio: {np.mean(extra_miss_ratio)}")
            print(f"Mean IoU (between stage2 objects): {np.mean(ious_stage2)}")
            eval_result = {
                "extra_miss_ratio": np.mean(extra_miss_ratio),
                "mean_iou_stage2": np.mean(ious_stage2)
            }
        if args.task == 'numeracy':
            print(f"Extra/Miss Ratio: {np.mean(extra_miss_ratio)}")
            print(f"Precision: {np.mean(precisions)}")
            print(f"Recall: {np.mean(recalls)}")
            print(f"Numeracy Accuracy: {np.mean(num_accs)}")
            print(f"Mean IoU (between stage2 objects): {np.mean(ious_stage2)}")
            eval_result = {
                "extra_miss_ratio": np.mean(extra_miss_ratio),
                "precision": np.mean(precisions),
                "recall": np.mean(recalls),
                "numeracy_accuracy": np.mean(num_accs),
                "mean_iou_stage2": np.mean(ious_stage2)
            }
        json.dump(eval_result, open(f"results/{YOLO_MODEL}_evaluation_result_{DIR[16:]}.json", "w"), indent=2)
