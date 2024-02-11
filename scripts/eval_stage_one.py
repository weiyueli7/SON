# This script allows evaluating stage one and saving the generated prompts to cache

import sys
import os
import numpy as np
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
eval_all_counts = {}
counter = []

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt-type", choices=prompt_types, default="demo")
    parser.add_argument("--model", choices=model_names, required=True)
    parser.add_argument("--template_version",
                        choices=template_versions, required=True)
    parser.add_argument("--skip_first_prompts", default=0, type=int)
    parser.add_argument("--num_prompts", default=None, type=int)
    parser.add_argument("--verbose", action='store_true')
    args = parser.parse_args()

    template_version = args.template_version

    model, llm_kwargs = get_llm_kwargs(
        model=args.model, template_version=template_version)

    cache.cache_format = "json"
    cache.cache_path = f'{os.getcwd()}/cache/cache_{args.prompt_type}_{template_version}_{model}.json'
    cache.init_cache()
    
    print(cache.cache_path)

    # prompts = get_prompts(args.prompt_type, model=model)
    with open(cache.cache_path, 'r') as f:
        prompts = json.load(f)

    print(f"Number of prompts: {len(prompts)}")

    for ind, prompt in enumerate(tqdm(prompts)):
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
        
        print("---------------------------------")
        print(f"Gen boxes: {gen_boxes}, bg_prompt: {bg_prompt}, neg_prompt: {neg_prompt}")
        total_overlap, total_object_area = calculate_overlapping_area_rate(gen_boxes)
        print(f"Total overlap: {total_overlap}, total object area: {total_object_area}")
        
        print("---------------------------------")
        
        object_areas.append(total_object_area)
        overlap_areas.append(total_overlap)
    
    print("Overlap Areas: ", overlap_areas)
    print("Object Areas: ", object_areas)
    
    print(f"Total overlap: {sum(overlap_areas)}, total object area: {sum(object_areas)}")
    print(f"Overlap rate: {sum(overlap_areas)/sum(object_areas)}")
        
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
