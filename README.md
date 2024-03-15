# SON: Enhancing Prompt Understanding of Diffusion Models with Large Language Models Guided Layouts


<a href='https://weiyueli7.github.io/SON/'><img src='https://img.shields.io/badge/Project-Page-Green'></a>  <a href=''><img src='https://img.shields.io/badge/Report-PDF-blue'> <a href=''><img src='https://img.shields.io/badge/Poster-PDF-red'> <a href='https://github.com/weiyueli7/SON/tree/main/data'><img src='https://img.shields.io/badge/SON-Dataset-yellow'>
# Getting Started 🚀

We provide instructions to run our code in this section.

## Installation
```
conda create -n SON python=3.8
conda activate SON
pip install -r requirements.txt
```
## Stage 1: Text-to-Layout Generation
**Note that we have uploaded the layout caches into this repo so that you can skip this step if you don't need layouts for new prompts.**

Since we have cached the layout generation (which will be downloaded when you clone the repo), **you need to remove the cache in `cache` directory if you want to re-generate the layout with the same prompts**.

**Our layout generation format:** The LLM takes in a text prompt describing the image and outputs three elements: **1.** captioned boxes, **2.** a background prompt, **3.** a negative prompt (useful if the LLM wants to express negation). The template and examples are in [prompt.py](prompt.py). You can edit the template and the parsing function to ask the LLM to generate additional things or even perform chain-of-thought for better generation.

### Option 1 (automated): Use an OpenAI API key
If you have an [OpenAI API key](https://openai.com/blog/openai-api), you can create a `utils/api_key.py` using the below format:

```python
import os

# You can either set `OPENAI_API_KEY` environment variable or replace "YOUR_API_KEY" below with your OpenAI API key
if "OPENAI_API_KEY" in os.environ:
    api_key = os.environ["OPENAI_API_KEY"]
else:
    api_key = "YOUR_API_KEY"
```

Put the API key in `utils/api_key.py` or set `OPENAI_API_KEY` environment variable. Then, you can use OpenAI's API for batch text-to-layout generation by querying an LLM, with GPT-4 as an example:

```
python prompt_batch.py --prompt-type demo --model gpt-4 --auto-query --always-save --template_version v0.1
```

`--prompt-type demo` includes a few prompts for demonstrations. The layout generation will be cached so it does not query the LLM again with the same prompt (lowers the cost).

You can visualize the bounding boxes in `img_generations/imgs_demo_templatev0.1`.

### Option 2 (free): Manually copy and paste to ChatGPT
```
python prompt_batch.py --prompt-type demo --model gpt-4 --always-save --template_version v0.1
```
Then copy and paste the template to [ChatGPT](https://chat.openai.com). Note that you want to use GPT-4 or change the `--model` to gpt-3.5 in order to match the cache file name. Then copy the response back. The generation will be cached.

If you want to visualize before deciding to save or not, you don't need to pass in `--always-save`.


### Run our SON-1K benchmark by tasks

We provide 3 tasks (spatial, numeracy, and complex natural prompts) in the benchmark. To generate the cache for the benchmark, run the following command:
```
python prompt_batch.py --prompt-type lmd_spatial --model gpt-4 --auto-query --always-save --template_version v0.1
```
You can replace `lmd_spatial` with `lmd_numeracy` or `lmd_complex` to generate the cache for the other tasks.

### Run our benchmark on text-to-layout generation evaluation
To evaluate the layout generation (spatial task as an example), run the following command.
```
python scripts/eval_stage_one.py --prompt-type lmd_spatial --model gpt-4 --template_version v0.1
```

## Stage 2: Layout-to-Image Generation
Note that since we provide caches for stage 1, you don't need to run stage 1 on your own for cached prompts that we provide (i.e., you don't need an OpenAI API key or to query an LLM).

Run layout-to-image generation using the gpt-4 cache and LMD+:
```
python generate.py --prompt-type lmd_spatial --model gpt-4 --save-suffix "gpt-4" --repeats 5 --frozen_step_ratio 0.5 --regenerate 1 --force_run_ind 0 --run-model lmd_plus --no-scale-boxes-default --template_version v0.1 --sdxl
```
With SD:
```
python generate.py --prompt-type lmd_spatial --model gpt-4 --save-suffix "gpt-4" --repeats 5  --regenerate 1 --force_run_ind 0 --run-model sd --no-scale-boxes-default --template_version v0.1
```
With MultiDiffusion:
```
python generate.py --prompt-type lmd_spatial --model gpt-4 --save-suffix "gpt-4" --repeats 5  --regenerate 1 --force_run_ind 0 --run-model multidiffusion --no-scale-boxes-default --template_version v0.1
```
With backward guidance:
```
python generate.py --prompt-type lmd_spatial --model gpt-4 --save-suffix "gpt-4" --repeats 5  --regenerate 1 --force_run_ind 0 --run-model backward_guidance --no-scale-boxes-default --template_version v0.1
```
With GLIGEN:
```
python generate.py --prompt-type lmd_spatial --model gpt-4 --save-suffix "gpt-4" --repeats 5  --regenerate 1 --force_run_ind 0 --run-model gligen --no-scale-boxes-default --template_version v0.1
```
With BoxDiff:
```
python generate.py --prompt-type lmd_spatial --model gpt-4 --save-suffix "gpt-4" --repeats 5  --regenerate 1 --force_run_ind 0 --run-model boxdiff --no-scale-boxes-default --template_version v0.1
```


### Run our benchmark on layout-to-image generation evaluation

To evaluate the layout-to-image generation (spatial task as an example), run the following command.
```shell
python evaluate_images.py --prompt_type lmd_spatial --task spatial --lm gpt-4 --template_version v0.1 --sdxl True --detection True
```

## Baseline model comparison
To run and compare our pipeline output with SDXL, tokencompose, or DALLE model, run the following command with correct model name and prompt file:

```shell
python baseline_generation.py --model sdxl --task lmd_spatial --prompt_file data/lmd_spatial.json
```

Evaluate the baseline model output with our evaluation script:

```shell
python evaluate_images.py --prompt_type lmd_spatial --task spatial --model_type sdxl --detection True
```






# Acknowledgements 🙏

We built upon the following repositories to create this project:
- [LLM-grounded Diffusion](https://github.com/TonyLianLong/LLM-groundedDiffusion)
- [diffusers](https://huggingface.co/docs/diffusers/index)
- [GLIGEN](https://github.com/gligen/GLIGEN)
- [layout-guidance](https://github.com/silent-chen/layout-guidance)
- [boxdiff](https://github.com/showlab/BoxDiff)
- [MultiDiffusion (region control)](https://github.com/omerbt/MultiDiffusion/tree/master)

Using their code means adhering to their license.
