# LMD: Enhancing Prompt Understanding of Text-to-Image Diffusion Models with Large Language Models Specilizing in Spatial Orientations

# Getting Started 🚀

We provide instructions to run our code in this section.

## Installation
```
conda create -n LMD python=3.8
conda activate LMD
pip install -r requirements.txt
```
## Stage 1: Text-to-Layout Generation
**Note that we have uploaded the layout caches into this repo so that you can skip this step if you don't need layouts for new prompts.**

Since we have cached the layout generation (which will be downloaded when you clone the repo), **you need to remove the cache in `cache` directory if you want to re-generate the layout with the same prompts**.

**Our layout generation format:** The LLM takes in a text prompt describing the image and outputs three elements: **1.** captioned boxes, **2.** a background prompt, **3.** a negative prompt (useful if the LLM wants to express negation). The template and examples are in [prompt.py](prompt.py). You can edit the template and the parsing function to ask the LLM to generate additional things or even perform chain-of-thought for better generation.

### Option 1 (automated): Use an OpenAI API key
If you have an [OpenAI API key](https://openai.com/blog/openai-api), you can put the API key in `utils/api_key.py` or set `OPENAI_API_KEY` environment variable. Then you can use OpenAI's API for batch text-to-layout generation by querying an LLM, with GPT-4 as an example:
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

### Run our benchmark on text-to-layout generation evaluation
We provide a benchmark that applies both to stage 1 and stage 2. This benchmarks includes a set of prompts with four tasks (negation, numeracy, attribute binding, and spatial relationships) as well as unified benchmarking code for all implemented methods and both stages.

This will generate layouts from the prompts in the benchmark (with `--prompt-type lmd`) and evaluate the results:
```
python prompt_batch.py --prompt-type demo --model gpt-4 --auto-query --always-save --template_version v0.1
python scripts/eval_stage_one.py --prompt-type demo --model gpt-4 --template_version v0.1
```
## Stage 2: Layout-to-Image Generation
Note that since we provide caches for stage 1, you don't need to run stage 1 on your own for cached prompts that we provide (i.e., you don't need an OpenAI API key or to query an LLM).

Run layout-to-image generation using the gpt-4 cache and LMD+:
```
python generate.py --prompt-type demo --model gpt-4 --save-suffix "gpt-4" --repeats 5 --frozen_step_ratio 0.5 --regenerate 1 --force_run_ind 0 --run-model lmd_plus --no-scale-boxes-default --template_version v0.1
```

`--save-suffix` is the suffix added to the name of the run. You can change that if you change the args to mark the setting in the runs. `--run-model` specifies the method to run. You can set to LMD/LMD+ or the implemented baselines (with examples below). Use `--use-sdv2` to enable SDv2.

### Run our benchmark on layout-to-image generation evaluation
We use a unified evaluation metric as stage 1 in stage 2 (`--prompt-type lmd`). Since we have layout boxes for stage 1 but only images for stage 2, we use OWL-ViT in order to detect the objects and ensure they are generated (or not generated in negation) in the right number, with the right attributes, and in the right place. This benchmark is still in beta stage.

This runs generation with LMD+ and evaluate the generation: 
```shell
# Use GPT-3.5 layouts
python generate.py --prompt-type lmd --model gpt-3.5 --save-suffix "gpt-3.5" --repeats 1 --frozen_step_ratio 0.5 --regenerate 1 --force_run_ind 0 --run-model lmd_plus --no-scale-boxes-default --template_version v0.1
python scripts/owl_vit_eval.py --model gpt-3.5 --run_base_path img_generations/img_generations_templatev0.1_lmd_plus_lmd_gpt-3.5/run0 --skip_first_prompts 0 --prompt_start_ind 0 --verbose --detection_score_threshold 0.15 --nms_threshold 0.15 --class-aware-nms
# Use GPT-4 layouts
python generate.py --prompt-type lmd --model gpt-4 --save-suffix "gpt-4" --repeats 1 --frozen_step_ratio 0.5 --regenerate 1 --force_run_ind 0 --run-model lmd_plus --no-scale-boxes-default --template_version v0.1
python scripts/owl_vit_eval.py --model gpt-4 --run_base_path img_generations/img_generations_templatev0.1_lmd_plus_lmd_gpt-4/run0 --skip_first_prompts 0 --prompt_start_ind 0 --verbose --detection_score_threshold 0.15 --nms_threshold 0.15 --class-aware-nms
```
## SDXL baseline model
To run and compare our pipeline output with SDXL model, run the following command with correct prompt file name:
```shell
# Example output for using demo_v0.1_gpt-4 cache prompt
python3 SDXL_baseline.py --prompt_file cache_demo_v0.1_gpt-4.json --cuda 0
```


# Acknowledgements 🙏

We built upon the following repositories to create this project:
- [LLM-grounded Diffusion](https://github.com/TonyLianLong/LLM-groundedDiffusion)
- [diffusers](https://huggingface.co/docs/diffusers/index)
- [GLIGEN](https://github.com/gligen/GLIGEN)
- [layout-guidance](https://github.com/silent-chen/layout-guidance)
- [boxdiff](https://github.com/showlab/BoxDiff)
- [MultiDiffusion (region control)](https://github.com/omerbt/MultiDiffusion/tree/master)
