# This script allows evaluating stage one and saving the generated prompts to cache

import sys
import re
import os
import numpy as np
import json
path_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(path_dir, '..'))

import json
import argparse
from prompt import get_prompts, prompt_types, template_versions
from utils.llm import get_llm_kwargs, get_parsed_layout, model_names
from utils.eval import get_eval_info_from_prompt, evaluate_with_boxes
from utils import cache
from tqdm import tqdm

def calculate_overlapping_area(objects):
    def overlap(rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
        overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
        return overlap_x * overlap_y
    total_overlap = 0
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            rect1 = objects[i]['bounding_box']
            rect2 = objects[j]['bounding_box']
            total_overlap += overlap(rect1, rect2)

    return total_overlap

def numeracy_evaluation(objects, text_objects):
    print(objects)
    print(text_objects)
    groud_truth = [obj[1] for obj in text_objects['num_object']]
    objects_keys = [re.sub(r'\s*\d+', '', obj['name']) for obj in objects]
    objects_keys = [obj[2:] if obj.startswith("a ") else obj[3:] if obj.startswith("an ") else obj for obj in objects_keys]
    prediction = [objects_keys.count(obj[0]) for obj in text_objects['num_object']]
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
        import subprocess
        subprocess.run("exit()", shell=True, check=True)
    # groud_truth = [obj[1] for obj in text_objects['num_object']]
    # objects_keys = [obj['name'] for obj in objects]
    # objects_keys = [obj[2:] if obj.startswith("a ") else obj[3:] if obj.startswith("an ") else obj for obj in objects_keys]
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


def spatial_evaluation(objects, text_objects):
    
    if len(objects) != len(text_objects['obj_attributes']):
        # print(objects)
        # print(text_objects['obj_attributes'])
        # import subprocess
        # subprocess.run("exit()", shell=True, check=True)
        return 0
    print(text_objects['obj_attributes'])
    print(objects)
    correct_order = []
    for idx, obj in enumerate(objects):
        name = ""
        if " of " in obj['name']:
            name = obj['name'].split(" of ")[1]
        elif obj['name'].startswith("a "):
            name = obj['name'][2:]#.strip()
        elif obj['name'].startswith("an "):
            name = obj['name'][3:]#.strip()
        else:
            name = obj['name']
        # print(name)
        # print(name.startswith("an "))
        correct_order.append(text_objects['obj_attributes'].index(name.lower()))
    rect = [objects[i]['bounding_box'] for i in correct_order]
    # rect = [objects[i]['bounding_box'] for i in range(len(text_objects['obj_attributes']))]
    # print(f"rect: {rect}")
    centroid = [[rect[i][0]+rect[i][2]//2, rect[i][1]+rect[i][3]//2] for i in range(len(text_objects['obj_attributes']))]
    # print(f"centroid: {centroid}")
    credit = 0
    # print("did not early stop")
    for i in range(len(text_objects['rel_type'])):
        relationship = []
        # if centroid[i][0] < centroid[i+1][0]:
        #     relationship += ["to the left of"]
        # if centroid[i][0] > centroid[i+1][0]:
        #     relationship += ["to the right of"]
        # if centroid[i][1] < centroid[i+1][1]:
        #     relationship += ["above"]
        # if centroid[i][1] > centroid[i+1][1]:
        #     relationship += ["below"]   
        d = euclidean_distance(centroid[i], centroid[i+1])
        print(d)
        print(centroid[i])
        print(centroid[i+1])
        if (centroid[i+1][1] - centroid[i][1])/d >= np.sin(np.pi/4):
            relationship += ["above"]
        if (centroid[i+1][1] - centroid[i][1])/d <= np.sin(-np.pi/4):
            relationship += ["below"]
        if (centroid[i][0] - centroid[i+1][0])/d >= np.cos(np.pi/4):
            relationship += ["to the right of"]
        if (centroid[i][0] - centroid[i+1][0])/d <= np.cos(3*np.pi/4):
            relationship += ["to the left of"]
        print(text_objects['rel_type'][i])
        print(relationship)
        if text_objects['rel_type'][i] in relationship:

            credit += 1
            
    return credit/len(text_objects['rel_type'])

def euclidean_distance(point1, point2):

    x1, y1 = point1
    x2, y2 = point2
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def calculate_overlapping_area_rate(objects):
    total_overlap = calculate_overlapping_area(objects)
    total_object_area = 0
    # print(objects)
    for obj in objects:
        total_object_area += obj['bounding_box'][2] * obj['bounding_box'][3]
    return total_overlap, total_object_area 

def eval_prompt(p, prompt_type, gen_boxes, verbose=False):
    # NOTE: we use the boxes from LLM
    texts, eval_info = get_eval_info_from_prompt(p, prompt_type)
    eval_type = eval_info["type"]
    eval_success = evaluate_with_boxes(gen_boxes, eval_info, verbose=verbose)
    overlap_area, object_area = calculate_overlapping_area_rate(gen_boxes)
    if len(gen_boxes) <= 2:
        overlap_area = 0
    return eval_type, eval_success, overlap_area, object_area, len(gen_boxes)


eval_success_counts = {}
overlap_areas = []
object_areas = []
spatial_check = {}
spatial_check['overall'] = []
spatial_check['fail'] = []

numeracy_check = {}
numeracy_check['precision'] = []
numeracy_check['recall'] = []
numeracy_check['accuracy'] = []
eval_all_counts = {}
counter = []

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt-type", choices=prompt_types, default="demo")
    parser.add_argument("--model", choices=model_names, required=True)
    parser.add_argument("--template_version",
                        choices=template_versions, required=True)
    parser.add_argument("--spatial_json", default="new_sample_3.json", type=str)
    parser.add_argument("--numeracy_json", default="numeracy.json", type=str)
    parser.add_argument("--complex_json", default="complex_prompt.json", type=str)
    parser.add_argument("--skip_first_prompts", default=0, type=int)
    parser.add_argument("--num_prompts", default=None, type=int)
    parser.add_argument("--verbose", action='store_true')
    args = parser.parse_args()

    template_version = args.template_version
 
    model, llm_kwargs = get_llm_kwargs(
        model=args.model, template_version=template_version)

    cache.cache_format = "json"
    if args.prompt_type.startswith("lmd"):
        cache.cache_path = f'{os.getcwd()}/cache/cache_{(args.prompt_type).split("lmd")[1][1:]}_{template_version}_{model}.json'
    else:
        cache.cache_path = f'{os.getcwd()}/cache/cache_{(args.prompt_type)}_{template_version}_{model}.json'
    if args.prompt_type.endswith("numeracy"):
        text_objects_path = f'{os.getcwd()}/data/{args.numeracy_json}'
    elif args.prompt_type.endswith("spatial"): #args.prompt_type.endswith("spatial"):
        text_objects_path = f'{os.getcwd()}/data/{args.spatial_json}'
    else:
        text_objects_path = f'{os.getcwd()}/data/{args.complex_json}'
    cache.init_cache()
    
    print(cache.cache_path)

    # prompts = get_prompts(args.prompt_type, model=model)
    with open(cache.cache_path, 'r') as f:
        prompts = json.load(f)
    with open(text_objects_path, 'r') as f:
        text_objects = json.load(f)

    print(f"Number of prompts: {len(prompts)}")

    for ind, prompt in enumerate(tqdm(prompts)):
        # if ind != 311:
        #     continue
        if isinstance(prompt, list):
            # prompt and kwargs
            prompt = prompt[0]
        prompt = prompt.strip().rstrip(".")
        if ind < args.skip_first_prompts:
            continue
        if args.num_prompts is not None and ind >= (args.skip_first_prompts + args.num_prompts):
            continue

        gen_boxes, bg_prompt, neg_prompt = get_parsed_layout(
            prompt, llm_kwargs, verbose=args.verbose)
        
        # print("---------------------------------")
        # print(f"Gen boxes: {gen_boxes}, bg_prompt: {bg_prompt}, neg_prompt: {neg_prompt}")
        total_overlap, total_object_area = calculate_overlapping_area_rate(gen_boxes)
        # print(f"Total overlap: {total_overlap}, total object area: {total_object_area}")

        # print("---------------------------------")
        if args.prompt_type.endswith("spatial"):
            cur_num_obj = text_objects[ind]['num_objects']
            check_spatial = spatial_evaluation(gen_boxes, text_objects[ind])
            if cur_num_obj not in spatial_check:
                spatial_check[cur_num_obj] = []
            spatial_check[cur_num_obj].append(check_spatial)
            spatial_check['overall'].append(check_spatial)
            if check_spatial == 0:
                spatial_check['fail'].append(ind)
        if args.prompt_type.endswith("numeracy"):
            numeracy_precision, numeracy_recall, numeracy_accuracy = numeracy_evaluation(gen_boxes, text_objects[ind])
            print(f"Precision: {numeracy_precision}, Recall: {numeracy_recall}, Accuracy: {numeracy_accuracy}")
            if text_objects[ind]['type'] != 'comparison':
                numeracy_check['recall'].append(numeracy_recall)
                numeracy_check['precision'].append(numeracy_precision)
            numeracy_check['accuracy'].append(numeracy_accuracy)
        if args.prompt_type.endswith("complex"):
            pass
                

        
        object_areas.append(total_object_area)
        overlap_areas.append(total_overlap)
        
    
    print("Overlap Areas: ", overlap_areas)
    print("Object Areas: ", object_areas)
    
    print(f"Total overlap: {sum(overlap_areas)}, total object area: {sum(object_areas)}")
    print(f"Overlap rate: {sum(overlap_areas)/sum(object_areas)}")
    if args.prompt_type.endswith("spatial"):
        spatial_results = {}
        spatial_results['overall'] = np.mean(spatial_check['overall'])
        print(f"Overall Spatial Accuracy: {np.mean(spatial_check['overall'])}")
        print(f"Spatial failed cases: {spatial_check['fail']}")
        print(f"Lowest Spatial Accuracy: {np.argmin(spatial_check['overall'])}")
        print(list(prompts)[int(np.argmin(spatial_check['overall']))])
        # for k, v in spatial_check.items():
        #     if k == 'overall' or k == 'fail':
        #         continue
        for i in range(3, 10):
            print(f"Spatial Accuracy for {i} objects: {np.mean(spatial_check[i])}")
            spatial_results[i] = np.mean(spatial_check[i])
        spatial_results['overlap_rate'] = sum(overlap_areas)/sum(object_areas)
        os.makedirs("results", exist_ok=True)
        json.dump(spatial_results, open(f"results/spatial_results_{template_version}_{model}.json", "w"), indent=2)
    if args.prompt_type.endswith("numeracy"):
        print(f"Overall Numeracy Precision: {np.mean(numeracy_check['precision'])}")
        print(f"Overall Numeracy Recall: {np.mean(numeracy_check['recall'])}")
        print(f"Overall Numeracy Accuracy: {np.mean(numeracy_check['accuracy'])}")
        numeracy_results = {}
        numeracy_results['precision'] = np.mean(numeracy_check['precision'])
        numeracy_results['recall'] = np.mean(numeracy_check['recall'])
        numeracy_results['accuracy'] = np.mean(numeracy_check['accuracy'])
        numeracy_results['overlap_rate'] = sum(overlap_areas)/sum(object_areas)
        os.makedirs("results", exist_ok=True)
        json.dump(numeracy_results, open(f"results/numeracy_results_{template_version}_{model}.json", "w"), indent=2)
    if args.prompt_type.endswith("complex"):
        complex_results = {}
        complex_results['overlap_rate'] = sum(overlap_areas)/sum(object_areas)
        os.makedirs("results", exist_ok=True)
        json.dump(complex_results, open(f"results/complex_results_{template_version}_{model}.json", "w"), indent=2)

    
    # THE BOTTOM LINE OF OUR IMPLEMENTATION
        
    #     eval_type, eval_success, overlap_area, object_area, num_object = eval_prompt(
    #         prompt, args.prompt_type, gen_boxes, verbose=args.verbose)
        
    #     print(eval_type)
        
    #     # print(f"object_area: {object_area}, overlap_area: {overlap_area}")

    #     print(f"Eval success (eval_type):", eval_success)

    #     if eval_type not in eval_all_counts:
    #         eval_success_counts[eval_type] = 0
    #         eval_all_counts[eval_type] = 0
    #         overlap_areas[eval_type] = 0
    #         object_areas[eval_type] = 0
    #     eval_success_counts[eval_type] += int(eval_success)
    #     eval_all_counts[eval_type] += 1
    #     overlap_areas[eval_type] += overlap_area
    #     object_areas[eval_type] += object_area
    #     counter += [num_object]

    # eval_success_conut, eval_all_count = 0, 0
    # for k, v in eval_all_counts.items():
    #     print(
    #         f"Eval type: {k}, success: {eval_success_counts[k]}/{eval_all_counts[k]}, rate: {eval_success_counts[k]/eval_all_counts[k]:.2f}")
    #     eval_success_conut += eval_success_counts[k]
    #     eval_all_count += eval_all_counts[k]
    # for k, v in overlap_areas.items():
    #     try:
    #         print(f"Eval type: {k}, overlap_area: {v}, object_area: {object_areas[k]}, rate: {v/object_areas[k]}")
    #     except:
    #         print(f"Eval type: {k}, overlap_area: {v}, rate: 0")
    # print(f"Number of Objects: {sum(counter)/400}")
    # print(f"Number of Scene with less than 3 Objects: {sum(np.array(counter) > 2)}")
    # print(f"Max Number of Objects: {max(np.array(counter))}")
    # print(
    #     f"Overall: success: {eval_success_conut}/{eval_all_count}, rate: {eval_success_conut/eval_all_count:.2f}")

    # if False:
    #     # Print what are accessed in the cache (may have multiple values in each key)
    #     # Not including the newly added items
    #     print(json.dumps(cache.cache_queries))
    #     print("Number of accessed keys:", len(cache.cache_queries))
