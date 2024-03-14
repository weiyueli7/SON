from diffusers import AutoPipelineForText2Image
from diffusers import StableDiffusionPipeline
from openai import OpenAI
from utils.api_key import api_key
import requests
import torch
from PIL import Image
import numpy as np
import argparse
import json
import os

def download_image(image_url, path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(f"{path}img_0.png", 'wb') as file:
            file.write(response.content)

def display(pipeline_text2image, prompt, save_prefix="", img_dir="baseline_img_generations", ind=None, save_ind_in_filename=True, client=None):
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
    if os.path.exists(f"{path}img_0.png"):
        print(f"The file {path} exists.")
    else:
        os.makedirs(path, exist_ok=True)
#         print(f"The file {path} does not exist.")
        if model_type == 'sdxl':
            image = pipeline_text2image(prompt=prompt, negative_target_size=(512, 512)).images[0]
        elif model_type == 'tokencompose':
            image = pipeline_text2image(prompt=prompt).images[0]
        elif model_type == "dalle-2":
            image = client.images.generate(
                        model="dall-e-2",
                        prompt=prompt,
                        size="512x512",
                        n=1,
                    ).data[0].url
        elif model_type == "dalle-3":
            image = client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size="1024x1024",
                        n=1,
                    ).data[0].url
        if model_type in ['sdxl', 'tokencompose']:
            if isinstance(image, np.ndarray):
                image = Image.fromarray(image)

            image.save(f"{path}img_0.png")
            torch.cuda.empty_cache()
            print(f"Saved to {path}img_0.png")
        elif model_type in ['dalle-2', 'dalle-3']:
            download_image(image, path)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--prompt_file', default="data/new_sample_3.json", help="prompt file path")
    parser.add_argument('--cuda', default="0", help="cuda number")
    parser.add_argument('--model', default='sdxl', help='which diffusion model to use (sdxl or tokencompose)')
    parser.add_argument('--task', default='lmd_spatial', help='which task to run (lmd_spatial or lmd_numeracy or lmd_complex)')
    args = parser.parse_args()
    prompt_file = args.prompt_file
    cuda = args.cuda
    model_type = args.model
 
    # torch.cuda.set_device(int(cuda.split(",")[0]))

    if model_type == 'sdxl':
        pipeline_text2image = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
        ).to("cuda")
        client = None
    elif model_type == 'tokencompose':
        pipeline_text2image = StableDiffusionPipeline.from_pretrained("mlpc-lab/TokenCompose_SD14_A", torch_dtype=torch.float32).to('cuda')
        client = None
    elif model_type == "dalle-2":
        pipeline_text2image = OpenAI(api_key=api_key)
        client = OpenAI(api_key=api_key)
    elif model_type == "dalle-3":
        pipeline_text2image = OpenAI(api_key=api_key)
        client = OpenAI(api_key=api_key)
    with open(f"{prompt_file}", 'r') as f:
        prompt_dict = json.load(f)
        
    idx = 0
    for k in prompt_dict:
        try:
            cur_prompt = k['prompt']
        except:
            cur_prompt = k['text']
        print(cur_prompt)
        display(pipeline_text2image, cur_prompt, save_prefix=f"{args.task}_{model_type}/{idx}/", ind=idx, client=client)
        idx += 1

