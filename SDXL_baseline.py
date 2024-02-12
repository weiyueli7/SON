from diffusers import AutoPipelineForText2Image
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
    if save_prefix != "":
        save_prefix = save_prefix + "_"
    if save_ind_in_filename:
        ind = f"{ind}_" if ind is not None else ""
        path = f"{img_dir}/{save_prefix}{ind}.png"
    else:
        ind = f"{ind}" if ind is not None else ""
        path = f"{img_dir}/{save_prefix}{ind}.png"
  
    
    if os.path.exists(path):
        print(f"The file {path} exists.")
    else:
        print(f"Saved to {path}")
#         print(f"The file {path} does not exist.")
    
        image = pipeline_text2image(prompt=prompt, negative_target_size=(512, 512)).images[0]

        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)

        image.save(path)
        torch.cuda.empty_cache()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-prompt_file', '--prompt_file', required=True, help="prompt file path")
    parser.add_argument('-cuda', '--cuda', required=True, help="cuda number")
    
    args = parser.parse_args()
    prompt_file = args.prompt_file
    cuda = args.cuda
    
    torch.cuda.set_device(int(cuda.split(",")[0]))

    pipeline_text2image = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
    ).to("cuda")

    with open(f"cache/{prompt_file}", 'r') as f:
        prompt_dict = json.load(f)
        
    idx = 0
    for k in prompt_dict:
        display(pipeline_text2image, k, save_prefix=prompt_file, ind=idx)
        idx += 1


