# The trailing space and "\n" is not a problem since they will be removed before making an API request.
templatev0_1 = """You are an intelligent bounding box generator. I will provide you with a caption for a photo, image, or painting. Your task is to generate the bounding boxes for the objects mentioned in the caption, along with a background prompt describing the scene. The images are of size 512x512. The top-left corner has coordinate [0, 0]. The bottom-right corner has coordinnate [512, 512]. The bounding boxes should not overlap or go beyond the image boundaries. Each bounding box should be in the format of (object name, [top-left x coordinate, top-left y coordinate, box width, box height]) and should not include more than one object. Do not put objects that are already provided in the bounding boxes into the background prompt. Do not include non-existing or excluded objects in the background prompt. Use "A realistic scene" as the background prompt if no background is given in the prompt. If needed, you can make reasonable guesses. Please refer to the example below for the desired format.

Caption: A realistic image of landscape scene depicting a green car parking on the left of a blue truck, with a red air balloon and a bird in the sky
Objects: [('a green car', [21, 281, 211, 159]), ('a blue truck', [269, 283, 209, 160]), ('a red air balloon', [66, 8, 145, 135]), ('a bird', [296, 42, 143, 100])]
Background prompt: A realistic landscape scene
Negative prompt: 

Caption: A realistic top-down view of a wooden table with two apples on it
Objects: [('a wooden table', [20, 148, 472, 216]), ('an apple', [150, 226, 100, 100]), ('an apple', [280, 226, 100, 100])]
Background prompt: A realistic top-down view
Negative prompt: 

Caption: A realistic scene of three skiers standing in a line on the snow near a palm tree
Objects: [('a skier', [5, 152, 139, 168]), ('a skier', [278, 192, 121, 158]), ('a skier', [148, 173, 124, 155]), ('a palm tree', [404, 105, 103, 251])]
Background prompt: A realistic outdoor scene with snow
Negative prompt: 

Caption: An oil painting of a pink dolphin jumping on the left of a steam boat on the sea
Objects: [('a steam boat', [232, 225, 257, 149]), ('a jumping pink dolphin', [21, 249, 189, 123])]
Background prompt: An oil painting of the sea
Negative prompt: 

Caption: A cute cat and an angry dog without birds
Objects: [('a cute cat', [51, 67, 271, 324]), ('an angry dog', [302, 119, 211, 228])]
Background prompt: A realistic scene
Negative prompt: birds

Caption: Two pandas in a forest without flowers
Objects: [('a panda', [30, 171, 212, 226]), ('a panda', [264, 173, 222, 221])]
Background prompt: A forest
Negative prompt: flowers

Caption: An oil painting of a living room scene without chairs with a painting mounted on the wall, a cabinet below the painting, and two flower vases on the cabinet
Objects: [('a painting', [88, 85, 335, 203]), ('a cabinet', [57, 308, 404, 201]), ('a flower vase', [166, 222, 92, 108]), ('a flower vase', [328, 222, 92, 108])]
Background prompt: An oil painting of a living room scene
Negative prompt: chairs

Caption: {prompt}
Objects: 
"""

templatev0_2 = """You are an intelligent 2D apartment floor plan designer. I will provide you with a caption for a floor plan image. Your task is to generate the bounding boxes for the furnitures mentioned in the caption, along with a background prompt describing the room layout. The images are of size 512x512. The top-left corner has coordinate [0, 0]. The bottom-right corner has coordinate [512, 512]. The bounding boxes should not overlap or go beyond the image boundaries. Each bounding box should be in the format of (furniture name, [top-left x coordinate, top-left y coordinate, box width, box height]) and should not include more than one furniture. Do not put furnitures that are already provided in the bounding boxes into the background prompt. Do not include non-existing or excluded furnitures in the background prompt. Use "A realistic floor plan image” as the background prompt if no background is given in the prompt. If needed, you can make reasonable guesses. Please refer to the example below for the desired format.

Caption: A realistic image of landscape scene depicting a green car parking on the left of a blue truck, with a red air balloon and a bird in the sky
Objects: [('a green car', [21, 281, 211, 159]), ('a blue truck', [269, 283, 209, 160]), ('a red air balloon', [66, 8, 145, 135]), ('a bird', [296, 42, 143, 100])]
Background prompt: A realistic landscape scene
Negative prompt: 

Caption: A realistic top-down view of a wooden table with two apples on it
Objects: [('a wooden table', [20, 148, 472, 216]), ('an apple', [150, 226, 100, 100]), ('an apple', [280, 226, 100, 100])]
Background prompt: A realistic top-down view
Negative prompt: 

Caption: A realistic scene of three skiers standing in a line on the snow near a palm tree
Objects: [('a skier', [5, 152, 139, 168]), ('a skier', [278, 192, 121, 158]), ('a skier', [148, 173, 124, 155]), ('a palm tree', [404, 105, 103, 251])]
Background prompt: A realistic outdoor scene with snow
Negative prompt: 

Caption: An oil painting of a pink dolphin jumping on the left of a steam boat on the sea
Objects: [('a steam boat', [232, 225, 257, 149]), ('a jumping pink dolphin', [21, 249, 189, 123])]
Background prompt: An oil painting of the sea
Negative prompt: 

Caption: A cute cat and an angry dog without birds
Objects: [('a cute cat', [51, 67, 271, 324]), ('an angry dog', [302, 119, 211, 228])]
Background prompt: A realistic scene
Negative prompt: birds

Caption: Two pandas in a forest without flowers
Objects: [('a panda', [30, 171, 212, 226]), ('a panda', [264, 173, 222, 221])]
Background prompt: A forest
Negative prompt: flowers

Caption: An oil painting of a living room scene without chairs with a painting mounted on the wall, a cabinet below the painting, and two flower vases on the cabinet
Objects: [('a painting', [88, 85, 335, 203]), ('a cabinet', [57, 308, 404, 201]), ('a flower vase', [166, 222, 92, 108]), ('a flower vase', [328, 222, 92, 108])]
Background prompt: An oil painting of a living room scene
Negative prompt: chairs

Caption: {prompt}
Objects: 
"""

templatev0_3 = """You are an intelligent bounding box generator. I will provide you with a caption for a photo, image, or painting. Your task is to generate the bounding boxes for the objects mentioned in the caption, along with a background prompt describing the scene. The images are of size 512x512. The top-left corner has coordinate [0, 0]. The bottom-right corner has coordinate [512, 512]. The bounding boxes should not overlap or go beyond the image boundaries. Each bounding box should be in the format of (object name, [top-left x coordinate, top-left y coordinate, box width, box height]) and should not include more than one object. The spatial relationship between any two objects should satisfy the following two relationships: Non-Overlapping Horizontal Space: For any two rectangles, the horizontal space occupied by one should not intersect with the horizontal space occupied by the other. This means that the right edge of the first rectangle should be to the left of the left edge of the second rectangle, or vice versa. Mathematically, for rectangles rect1 = (x1, y1, w1, h1) and rect2 = (x2, y2, w2, h2), this condition can be expressed as either x1 + w1 <= x2 or x2 + w2 <= x1. Non-Overlapping Vertical Space: Similarly, for the vertical space, the bottom edge of the first rectangle should be above the top edge of the second rectangle, or vice versa. In terms of coordinates, for the same rectangles rect1 and rect2, this condition is met if either y1 + h1 <= y2 or y2 + h2 <= y1. Do not put objects that are already provided in the bounding boxes into the background prompt. Do not include non-existing or excluded objects in the background prompt. Use "A realistic scene" as the background prompt if no background is given in the prompt. If needed, you can make reasonable guesses. Please refer to the example below for the desired format.

Caption: A realistic image of landscape scene depicting a green car parking on the left of a blue truck, with a red air balloon and a bird in the sky
Objects: [('a green car', [21, 281, 211, 159]), ('a blue truck', [269, 283, 209, 160]), ('a red air balloon', [66, 8, 145, 135]), ('a bird', [296, 42, 143, 100])]
Background prompt: A realistic landscape scene
Negative prompt: 

Caption: A realistic top-down view of a wooden table with two apples on it
Objects: [('a wooden table', [20, 148, 472, 216]), ('an apple', [150, 226, 100, 100]), ('an apple', [280, 226, 100, 100])]
Background prompt: A realistic top-down view
Negative prompt: 

Caption: A realistic scene of three skiers standing in a line on the snow near a palm tree
Objects: [('a skier', [5, 152, 139, 168]), ('a skier', [278, 192, 121, 158]), ('a skier', [148, 173, 124, 155]), ('a palm tree', [404, 105, 103, 251])]
Background prompt: A realistic outdoor scene with snow
Negative prompt: 

Caption: An oil painting of a pink dolphin jumping on the left of a steam boat on the sea
Objects: [('a steam boat', [232, 225, 257, 149]), ('a jumping pink dolphin', [21, 249, 189, 123])]
Background prompt: An oil painting of the sea
Negative prompt: 

Caption: A cute cat and an angry dog without birds
Objects: [('a cute cat', [51, 67, 271, 324]), ('an angry dog', [302, 119, 211, 228])]
Background prompt: A realistic scene
Negative prompt: birds

Caption: Two pandas in a forest without flowers
Objects: [('a panda', [30, 171, 212, 226]), ('a panda', [264, 173, 222, 221])]
Background prompt: A forest
Negative prompt: flowers

Caption: An oil painting of a living room scene without chairs with a painting mounted on the wall, a cabinet below the painting, and two flower vases on the cabinet
Objects: [('a painting', [88, 85, 335, 203]), ('a cabinet', [57, 308, 404, 201]), ('a flower vase', [166, 222, 92, 108]), ('a flower vase', [328, 222, 92, 108])]
Background prompt: An oil painting of a living room scene
Negative prompt: chairs

Caption: {prompt}
Objects: 
"""

DEFAULT_SO_NEGATIVE_PROMPT = "artifacts, blurry, smooth texture, bad quality, distortions, unrealistic, distorted image, bad proportions, duplicate, two, many, group, occlusion, occluded, side, border, collate"
DEFAULT_OVERALL_NEGATIVE_PROMPT = "artifacts, blurry, smooth texture, bad quality, distortions, unrealistic, distorted image, bad proportions, duplicate"

templates = {"v0.1": templatev0_1, "v0.2": templatev0_2, "v0.3": templatev0_3}
template_versions = ["v0.1", "v0.2", "v0.3"]

stop = "\n\n"


prompts_demo_gpt4, prompts_demo_gpt3_5 = [], []

# Put what we want to generate when you query GPT-4 for demo here
prompts_demo_gpt4 = [
    # "In an indoor scene, a blue cube directly above a red cube with a vase on the left of them.",
    # "A realistic photo of a wooden table without bananas in an indoor scene",
    # "A realistic image of a white deer and a gray bear in an empty factory scene",
    
    
    # "A surreal scene of three red umbrellas floating above a calm lake, with no boats, where the middle umbrella is higher than the others.",
    # "An image of two orange cats sitting on a blue sofa in a living room, without any plants, with one cat on the left end and the other on the right.",
    # "A vibrant street scene with five bicycles leaning against a yellow wall, excluding any pedestrians, with bicycles arranged in size order from left to right.",
    # "An underwater image of four dolphins swimming around a sunken ship, but no sharks present, with two dolphins above the ship and two below.",
    # "A peaceful forest clearing with seven different colored butterflies, without any birds, where butterflies form a circular pattern in the air.",
    # "A snowy landscape featuring two large pine trees and a small wooden cabin, but no animals, with the cabin situated between the trees.",
    # "A fantasy image of three flying carpets over a desert, with no clouds in the sky, where the carpets are flying in a vertical line, one above the other.",
    # "A busy kitchen scene with five chefs cooking, but no kitchen utensils visible, where the chefs are evenly spaced around a large table.",
    # "An image of a garden with six different flower beds in bloom, without any garden furniture, where the flower beds form a hexagon shape.",
    # "A bustling city street with four food trucks, excluding any cars, lined up side by side, each truck a different color.",
    # "An image of a beach at sunset with three palm trees, but no people, where the trees are spaced evenly along the shoreline.",
    # "A mountain scene with two eagles soaring, but no other birds, where one eagle is higher than the other against a clear sky.",
    # "An old library interior with seven bookshelves, without any tables or chairs, where the bookshelves form a U-shape around the room.",
    # "A starry night sky with five shooting stars, but no moon, where the stars all originate from the same point in the sky.",
    # "A winter village scene with four houses covered in snow, without any snowmen, where the houses are arranged in a square formation.",
    # "A serene pond with three lotus flowers blooming, excluding any fish, where the flowers are at different stages of bloom.",
    # "An image of a train station with two trains on adjacent tracks, but no passengers, where one train is longer than the other.",
    # "A meadow scene at sunrise with five horses grazing, but no trees, where the horses are evenly spaced across the meadow.",
    # "A space scene with three planets aligned in a row, but no stars, where each planet is a different color and size.",
    # "An art studio with four easels holding unfinished paintings, without any artists, where the easels are positioned in a semi-circle."


#     "In a bustling downtown area during evening rush, a person leans against a streetlight, waiting to cross the road. Nearby, a parked motorcycle reflects the fading light, while a city bus halts at a designated stop. Across the street, a bicycle is securely locked to a bike rack, and a stray cat watches the busy scene from a safe distance.",
# "Along a peaceful riverbank, a couple (two people) relax on a bench, enjoying the view. A carefully parked bicycle leans against a nearby tree. A playful dog runs around, occasionally chasing birds that land near the water's edge. In the background, a boat slowly cruises down the river.",
# "In a suburban neighborhood, a person jogs past a row of houses, each with a car in the driveway. At a nearby house, a dog barks from the yard, drawing the attention of a bird perched on the mailbox. On the sidewalk, a child's abandoned bicycle lies next to a fire hydrant.",
# "A lively city park scene where a person reads a book on a bench under a tree. Nearby, a mother and child (two people) play frisbee on the grass. A curious squirrel (animal) scampers around, occasionally stopping to observe. In the distance, a parked motorcycle and a bicycle stand by a park entrance.",
# "On a rustic farmstead, a person feeds chickens near a barn. A few sheep graze in an adjacent paddock, while a horse stands by the fence, watching a passing train in the distance. Near the farmhouse, a truck is parked, with its headlights reflecting off a nearby water trough."
"A serene park scene with a bench, a bicycle leaning against a nearby tree, a playful dog chasing a frisbee, and a distant cat observing from atop a wall.",
    "A bustling city street featuring a car waiting at a traffic light, a bus passing by, a pedestrian carrying an umbrella, and a taxi parked by a fire hydrant.",
    "A cozy living room with a couch, a coffee table holding a remote and a cup, a tv on a stand, and a cat sleeping on a nearby rug."
]

# Put what we want to generate when you query GPT-3.5 for demo here
prompts_demo_gpt3_5 = []

prompt_types = [
    "demo",
    "lmd_negation",
    "lmd_numeracy",
    "lmd_attribution",
    "lmd_spatial",
    "lmd",
]


def get_prompts(prompt_type, model, allow_non_exist=False):
    """
    This function returns the text prompts according to the requested `prompt_type` and `model`. Set `model` to "all" to return all the text prompts in the current type. Otherwise we may want to have different prompts for gpt-3.5 and gpt-4 to prevent confusion.
    """
    prompts_gpt4, prompts_gpt3_5 = {}, {}
    if prompt_type.startswith("lmd"):
        # from utils.eval.lmd import get_lmd_prompts

        # prompts = get_lmd_prompts()
        import json
        import numpy as np
        data = json.load(open("data/text_spatial_rel_phrases.json"))
        all_spatial_rel_phrases = {'above', 'below', 'to the left of', 'to the right of'}
        two_objs_data = []
        two_objs_data_above = []
        two_objs_data_below = []
        two_objs_data_left = []
        two_objs_data_right = []
        for d in data:
            if d['rel_type'] in all_spatial_rel_phrases:
                two_objs_data.append(d)
                if d['rel_type'] == 'above':
                    two_objs_data_above.append(d)
                elif d['rel_type'] == 'below':
                    two_objs_data_below.append(d)
                elif d['rel_type'] == 'to the left of':
                    two_objs_data_left.append(d)
                elif d['rel_type'] == 'to the right of':
                    two_objs_data_right.append(d)
        np.random.seed(0)
        samples_below = np.random.choice(two_objs_data_below, 100, replace=False)
        samples_above = np.random.choice(two_objs_data_above, 100, replace=False)
        samples_left = np.random.choice(two_objs_data_left, 100, replace=False)
        samples_right = np.random.choice(two_objs_data_right, 100, replace=False)
        samples = list(np.concatenate([samples_below, samples_above, samples_left, samples_right]))
        prompts = {'lmd_spatial': [d['text'] for d in samples]}
        # print(prompts)
        # We do not add to both dict to prevent duplicates when model is set to "all".
        if "gpt-4" in model:
            prompts_gpt4.update(prompts)
        else:
            prompts_gpt3_5.update(prompts)
    elif prompt_type == "demo":
        prompts_gpt4["demo"] = prompts_demo_gpt4
        prompts_gpt3_5["demo"] = prompts_demo_gpt3_5

    if "all" in model:
        return prompts_gpt4.get(prompt_type, []) + prompts_gpt3_5.get(prompt_type, [])
    elif "gpt-4" in model:
        if allow_non_exist:
            return prompts_gpt4.get(prompt_type, [])
        return prompts_gpt4[prompt_type]
    else:
        # Default: gpt-3.5
        if allow_non_exist:
            return prompts_gpt3_5.get(prompt_type, [])
        return prompts_gpt3_5[prompt_type]


if __name__ == "__main__":
    # Print the full prompt for the latest prompt in prompts
    # This allows pasting into an LLM web UI
    prompt_type = "demo"

    assert prompt_type in prompt_types, f"prompt_type {prompt_type} does not exist"

    prompts = get_prompts(prompt_type, "all")
    prompt = prompts[-1]

    #prompt_full = templatev0_1.format(prompt=prompt.strip().rstrip("."))
    prompt_full = templatev0_2.format(prompt=prompt.strip().rstrip("."))
    print(prompt_full)

    if False:
        # Useful if you want to query an LLM with JSON input
        
        import json

        print(json.dumps(prompt_full.strip("\n")))