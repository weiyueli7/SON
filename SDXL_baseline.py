from diffusers import AutoPipelineForText2Image
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import numpy as np
import argparse
import json
import os

def display(pipeline_text2image, prompt, save_prefix="", img_dir="SDXL_output", ind=None, save_ind_in_filename=True):
    """
    save_ind_in_filename: This adds a global index to the filename so that two calls to this function will not save to the same file and overwrite the previous image.
    """
    # if save_prefix != "":
    #     save_prefix = save_prefix #+ "_"
    # if save_ind_in_filename:
    #     ind = f"{ind}" if ind is not None else ""
    #     path = f"{img_dir}/{save_prefix}"
    # else:
    #     ind = f"{ind}" if ind is not None else ""
    path = f"{img_dir}/{save_prefix}"
  
    
    if os.path.exists(f"{path}img_0.pnd"):
        print(f"The file {path} exists.")
    else:
        
        os.makedirs(path, exist_ok=True)
#         print(f"The file {path} does not exist.")
        if model_type == 'sdxl':
            image = pipeline_text2image(prompt=prompt, negative_target_size=(512, 512)).images[0]
        elif model_type == 'tokencompose':
            image = pipeline_text2image(prompt=prompt).images[0]

        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)

        image.save(f"{path}img_0.png")
        torch.cuda.empty_cache()
        print(f"Saved to {path}img_0.png")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # parser.add_argument('-prompt_file', '--prompt_file', required=True, help="prompt file path")
    # parser.add_argument('-cuda', '--cuda', required=True, help="cuda number")
    parser.add_argument('--prompt_file', default="data/new_sample_3.json", help="prompt file path")
    parser.add_argument('--cuda', default="0", help="cuda number")
    parser.add_argument('--model', default='sdxl', help='which diffusion model to use (sdxl or tokencompose)')
    
    args = parser.parse_args()
    prompt_file = args.prompt_file
    cuda = args.cuda
    model_type = args.model
    
    torch.cuda.set_device(int(cuda.split(",")[0]))

    if model_type == 'sdxl':
        
        pipeline_text2image = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
        ).to("cuda")
    elif model_type == 'tokencompose':
        pipeline_text2image = StableDiffusionPipeline.from_pretrained("mlpc-lab/TokenCompose_SD14_A", torch_dtype=torch.float32).to('cuda')

    with open(f"{prompt_file}", 'r') as f:
        prompt_dict = json.load(f)
        
    idx = 0
    for k in prompt_dict:
        cur_prompt = k['text']
        print(cur_prompt)
        display(pipeline_text2image, cur_prompt, save_prefix=f"spatial_{model_type}/{idx}/", ind=idx)
        idx += 1
        # break


