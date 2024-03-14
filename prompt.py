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

templatev0_2 = """You are an intelligent bounding box generator. I will provide you with a description of a photo, scene, or painting. Your task is to generate the bounding boxes for the objects mentioned in the description, along with a background prompt describing the scene. The images are of size 512x512. The top-left corner has coordinates [0, 0]. The bottom-right corner has coordinates [512, 512]. The bounding boxes should not overlap or go beyond the image boundaries. Each bounding box should be in the format of (object name, [top-left x coordinate, top-left y coordinate, box width, box height]) and should not include more than one object. The spatial relationship between any two objects should satisfy the following two relationships: 1. Non-Overlapping Horizontal Space: For any two rectangles, the horizontal space occupied by one should not intersect with the horizontal space occupied by the other. This means that the right edge of the first rectangle should be to the left of the left edge of the second rectangle, or vice versa. Mathematically, for rectangles rect1 = (x1, y1, w1, h1) and rect2 = (x2, y2, w2, h2), this condition can be expressed as either x1 + w1 <= x2 or x2 + w2 <= x1. 2. Non-Overlapping Vertical Space: Similarly, for vertical space, the bottom edge of the first rectangle should be above the top edge of the second rectangle, or vice versa. In terms of coordinates, for the same rectangles rect1 and rect2, this condition is met if either y1 + h1 <= y2 or y2 + h2 <= y1.
Pay attention to the keywords that indicate the spatial relationship (“left”, “right”, “above”, and “below”) between objects and we will use the centroid (x for left or right; y for above or below) of the bounding box for each object to validate their spatial relationship. Suppose we have objects A and B with coordinates (x1, y1, w1, h1) and (x2, y2, w2, h2), then “A is to the left of B” must satisfy (centroid x of A) < (centroid x of B) where (centroid x of A) is calculated by (x1 + w1//2).
Do not put objects that are already provided in the bounding boxes into the background prompt. Do not include non-existing or excluded objects in the background prompt.
Use "A realistic scene" as the background prompt if no background is given in the prompt. If needed, you can make reasonable guesses. Please refer to the example below for the desired format.

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

templatev0_4 = """You are an intelligent bounding box generator. I will provide you with a description of a photo, scene, or painting. Your task is to generate the bounding boxes for the objects mentioned in the description, along with a background prompt describing the scene. The images are of size 512x512. The top-left corner has coordinates [0, 0]. The bottom-right corner has coordinates [512, 512]. The bounding boxes should not overlap or go beyond the image boundaries. Each bounding box should be in the format of (object name, [top-left x coordinate, top-left y coordinate, box width, box height]) and should not include more than one object. 
To prevent overlap, for any two boxes (box1 and box2), the conditions (x1 + w1 <= x2) or (x2 + w2 <= x1) for the x-coordinates or (y1 + h1 <= y2) or (y2 + h2 <= y1) for the y-coordinates must be met.
Furthermore, if the description uses spatial keywords ('left', 'right', 'above', 'below'), the positioning of the bounding boxes must reflect these relationships accurately. This means adjusting the centroids of the boxes (cx1, cy1 for box1; cx2, cy2 for box2) so that: cx1 < cx2 if Object A is to the left of B; cx1 > cx2 if A is to the right of B; cy1 < cy2 if A is above B; and cy1 > cy2 if A is below B. Centroids are calculated as cx = x + w//2 and cy = y + h//2.
Objects defined within the bounding boxes should not be repeated in the scene's background description. Exclude any non-relevant or omitted objects from this background narrative. Use "A realistic scene" as the background prompt if no background is given in the prompt. If needed, you can make reasonable guesses. Please refer to the example below for the desired format.

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

templatev0_5 = """You are an intelligent bounding box generator. I will provide you with a description of a photo, scene, or painting. Your task is to generate the bounding boxes for the objects mentioned in the description, along with a background prompt describing the scene. The images are of size 512x512. The top-left corner has coordinates [0, 0]. The bottom-right corner has coordinates [512, 512]. The bounding boxes should not overlap or go beyond the image boundaries. Each bounding box should be in the format of (object name, [top-left x coordinate, top-left y coordinate, box width, box height]) and should not include more than one object. 
To prevent overlap, for any two boxes (box1 and box2), the conditions (x1 + w1 <= x2) or (x2 + w2 <= x1) for the x-coordinates or (y1 + h1 <= y2) or (y2 + h2 <= y1) for the y-coordinates must be met.
Furthermore, if the description uses spatial keywords ('left', 'right', 'above', 'below'), the positioning of the bounding boxes must reflect these relationships accurately. This means adjusting the centroids of the boxes (cx1, cy1 for box1; cx2, cy2 for box2) so that: cx1 < cx2 if Object A is to the left of B; cx1 > cx2 if A is to the right of B; cy1 < cy2 if A is above B; and cy1 > cy2 if A is below B. Centroids are calculated as cx = x + w//2 and cy = y + h//2.
Objects defined within the bounding boxes should not be repeated in the scene's background description. Exclude any non-relevant or omitted objects from this background narrative. Use "A realistic scene" as the background prompt if no background is given in the prompt. If needed, you can make reasonable guesses. Please refer to the example below for the desired format.

Caption: A realistic image of landscape scene depicting a green car parking on the left of a blue truck, with a red air balloon and a bird in the sky
Objects: [('a green car', [21, 281, 211, 159]), ('a blue truck', [269, 283, 209, 160]), ('a red air balloon', [66, 8, 145, 135]), ('a bird', [296, 42, 143, 100])]
Background prompt: A realistic landscape scene
Negative prompt:

<Begin Explanation>

Caption Analysis: The scene describes a realistic landscape with specific spatial relations:
A green car is parked on the left of a blue truck.
A red air balloon and a bird are in the sky.

Given these details, we need to ensure the bounding boxes for these objects adhere to their described spatial relationships and that they're appropriately placed within the context of a landscape scene.

Bounding Boxes:
Green Car: [21, 281, 211, 159]
Positioned starting at x=21, y=281 with a width of 211 and a height of 159.
The car's centroid can be calculated as (x + w/2, y + h/2) = (126.5, 360.5).
Blue Truck: [269, 283, 209, 160]
Positioned starting at x=269, y=283 with a width of 209 and a height of 160.
The truck's centroid can be calculated as (373.5, 363).
Red Air Balloon: [66, 8, 145, 135]
Positioned starting at x=66, y=8 with a width of 145 and a height of 135.
The air balloon's centroid can be calculated as (138.5, 75.5).
Bird: [296, 42, 143, 100]
Positioned starting at x=296, y=42 with a width of 143 and a height of 100.
The bird's centroid can be calculated as (367.5, 92).

Analysis of Adherence:
Spatial Relationship Between Car and Truck:
The green car's centroid is at x=126.5, and the blue truck's centroid is at x=373.5. This means the green car is to the left of the blue truck, which adheres to the caption.
Objects in the Sky:
Both the red air balloon and the bird are positioned with low y-values (8 and 42, respectively), indicating they are in the sky, adhering to the caption's description.
Non-Overlapping and Within Boundaries:
The provided coordinates ensure that none of the bounding boxes overlap with one another, and all are within the 512x512 boundary.

Conclusion:
The objects and their coordinates adhere to the scene caption accurately, respecting the spatial relationships and placements as described. The scene's objects are correctly positioned to reflect the narrative of a green car parked to the left of a blue truck, with a red air balloon and a bird positioned in the sky, maintaining the integrity of a realistic landscape scene.

<End Explanation>

Caption: A realistic top-down view of a wooden table with two apples on it
Objects: [('a wooden table', [20, 148, 472, 216]), ('an apple', [150, 226, 100, 100]), ('an apple', [280, 226, 100, 100])]
Background prompt: A realistic top-down view
Negative prompt: 

<Begin Explanation>

Caption Analysis: The scene is a top-down view featuring:
A wooden table.
Two apples positioned on the table.

Bounding Boxes:
Wooden Table: [20, 148, 472, 216]
Positioned starting at x=20, y=148 with a width of 472 and a height of 216.
The table's coverage is extensive, suggesting it's the primary object in the scene.
First Apple: [150, 226, 100, 100]
Positioned starting at x=150, y=226 with a width and height of 100.
This square shape is appropriate for an apple in a top-down view.
Second Apple: [280, 226, 100, 100]
Positioned starting at x=280, y=226 with a width and height of 100.
Similar to the first apple, indicating consistency in depiction.

Analysis of Adherence:
Table Placement and Size:
The table occupies a significant portion of the scene, which is expected in a top-down view. Its large width (472) relative to its height (216) suggests a surface area large enough to hold objects, fitting the description of a wooden table.
Apples on the Table:
Both apples are placed with their top-left corners at y=226, which is within the table's y-range (148 to 364). This confirms they are on the table. Their x-coordinates (150 and 280) and sizes (100x100) ensure they are distinct objects on the table without overlapping, adhering to the realistic depiction.
Spatial Relationship Between Apples:
The apples are placed next to each other horizontally (as indicated by their x-coordinates and the absence of y-coordinate variance), which is an expected arrangement for objects on a table in a top-down view.

Conclusion:
The objects and their coordinates accurately adhere to the scene caption. The wooden table's size and placement provide a broad, realistic surface for the apples. The apples are depicted as distinct, non-overlapping objects on the table, positioned in a way that is logical for a top-down view. This setup effectively creates a realistic depiction of a wooden table with two apples on it, viewed from above.

<End Explanation>


Caption: A realistic scene of three skiers standing in a line on the snow near a palm tree
Objects: [('a skier', [5, 152, 139, 168]), ('a skier', [278, 192, 121, 158]), ('a skier', [148, 173, 124, 155]), ('a palm tree', [404, 105, 103, 251])]
Background prompt: A realistic outdoor scene with snow
Negative prompt: 

<Begin Explanation>

Caption Analysis: The scene describes a realistic outdoor snowy landscape with the following details:
Three skiers standing in a line.
A palm tree is present near the skiers.
Given these details, we need to ensure the bounding boxes for these objects adhere to their described spatial relationships within an outdoor snowy scene.

Bounding Boxes:
First Skier: [5, 152, 139, 168]
Positioned starting at x=5, y=152 with a width of 139 and a height of 168.
Second Skier: [278, 192, 121, 158]
Positioned starting at x=278, y=192 with a width of 121 and a height of 158.
Third Skier: [148, 173, 124, 155]
Positioned starting at x=148, y=173 with a width of 124 and a height of 155.
Palm Tree: [404, 105, 103, 251]
Positioned starting at x=404, y=105 with a width of 103 and a height of 251.

Analysis of Adherence:
Skiers in a Line:
The skiers are positioned in a way that could represent a line, but the sequence based on their x-coordinates seems to be out of order for a straight line formation. The correct order should reflect their positions as increasing in x-values without overlapping, ideally with the first skier having the lowest x-value, followed by the third, and then the second based on their current coordinates. However, their current arrangement (first, third, and then second) does somewhat maintain a line but not in the straightest or most orderly manner.
Near a Palm Tree:
The palm tree, with its starting x-coordinate at 404, is positioned to the right of all skiers. This placement adheres to the scene description, implying that the palm tree is near the skiers but does not specify which side. Given the broad interpretation of "near," this condition is met.

Conclusion:
While the skiers are not perfectly aligned in a straight line according to their x-coordinates, they are positioned sequentially from left to right, which could be interpreted as standing "in a line" from a less strict perspective. The palm tree is correctly placed to the side of the skiers, which aligns with the description. Therefore, the objects and their coordinates largely adhere to the scene caption, capturing a realistic outdoor scene with snow, three skiers, and a palm tree, albeit with some flexibility in interpreting the exact positioning of the skiers in relation to each other.

<End Explanation>

Caption: {prompt}
Objects: 
"""

templatev0_6 = """You are an intelligent bounding box generator. I will provide you with a description of a photo, scene, or painting. Your task is to generate the bounding boxes for the objects mentioned in the description, along with a background prompt describing the scene. The images are of size 512x512. The top-left corner has coordinates [0, 0]. The bottom-right corner has coordinates [512, 512]. The bounding boxes should not overlap or go beyond the image boundaries. Each bounding box should be in the format of (object name, [top-left x coordinate, top-left y coordinate, box width, box height]) and should not include more than one object. 
To prevent overlap, for any two boxes (box1 and box2), the conditions (x1 + w1 <= x2) or (x2 + w2 <= x1) for the x-coordinates or (y1 + h1 <= y2) or (y2 + h2 <= y1) for the y-coordinates must be met.
Furthermore, if the description uses spatial keywords ('left', 'right', 'above', 'below'), the positioning of the bounding boxes must reflect these relationships accurately. This means adjusting the centroids of the boxes (cx1, cy1 for box1; cx2, cy2 for box2) so that: cx1 < cx2 if Object A is to the left of B; cx1 > cx2 if A is to the right of B; cy1 < cy2 if A is above B; and cy1 > cy2 if A is below B. Centroids are calculated as cx = x + w//2 and cy = y + h//2.
Objects defined within the bounding boxes should not be repeated in the scene's background description. Exclude any non-relevant or omitted objects from this background narrative. Use "A realistic scene" as the background prompt if no background is given in the prompt. If needed, you can make reasonable guesses. Please refer to the example below for the desired format.

<Scene One Begin>
Caption: A realistic image of landscape scene depicting a green car parking on the left of a blue truck, with a red air balloon and a bird in the sky
Objects: [('a green car', [21, 281, 211, 159]), ('a blue truck', [269, 283, 209, 160]), ('a red air balloon', [66, 8, 145, 135]), ('a bird', [296, 42, 143, 100])]
Background prompt: A realistic landscape scene
Negative prompt:
<Scene One End>

Why does Scene One's layout have no overlapping and adhere to the caption's description of spatial relationships? Please provide an explanation.

<Begin Explanation>

Caption Analysis: The scene describes a realistic landscape with specific spatial relations:
A green car is parked on the left of a blue truck.
A red air balloon and a bird are in the sky.

Given these details, we need to ensure the bounding boxes for these objects adhere to their described spatial relationships and that they're appropriately placed within the context of a landscape scene.

Bounding Boxes:
Green Car: [21, 281, 211, 159]
Positioned starting at x=21, y=281 with a width of 211 and a height of 159.
The car's centroid can be calculated as (x + w/2, y + h/2) = (126.5, 360.5).
Blue Truck: [269, 283, 209, 160]
Positioned starting at x=269, y=283 with a width of 209 and a height of 160.
The truck's centroid can be calculated as (373.5, 363).
Red Air Balloon: [66, 8, 145, 135]
Positioned starting at x=66, y=8 with a width of 145 and a height of 135.
The air balloon's centroid can be calculated as (138.5, 75.5).
Bird: [296, 42, 143, 100]
Positioned starting at x=296, y=42 with a width of 143 and a height of 100.
The bird's centroid can be calculated as (367.5, 92).

Analysis of Adherence:
Spatial Relationship Between Car and Truck:
The green car's centroid is at x=126.5, and the blue truck's centroid is at x=373.5. This means the green car is to the left of the blue truck, which adheres to the caption.
Objects in the Sky:
Both the red air balloon and the bird are positioned with low y-values (8 and 42, respectively), indicating they are in the sky, adhering to the caption's description.
Non-Overlapping and Within Boundaries:
The provided coordinates ensure that none of the bounding boxes overlap with one another, and all are within the 512x512 boundary.

Conclusion:
The objects and their coordinates adhere to the scene caption accurately, respecting the spatial relationships and placements as described. The scene's objects are correctly positioned to reflect the narrative of a green car parked to the left of a blue truck, with a red air balloon and a bird positioned in the sky, maintaining the integrity of a realistic landscape scene.

<End Explanation>

<Scene Two Begin>
Caption: A realistic top-down view of a wooden table with two apples on it
Objects: [('a wooden table', [20, 148, 472, 216]), ('an apple', [150, 226, 100, 100]), ('an apple', [280, 226, 100, 100])]
Background prompt: A realistic top-down view
Negative prompt: 
<Scene Two End>

Why does Scene Two's layout have no overlapping and adhere to the caption's description of spatial relationships? Please provide an explanation.

<Begin Explanation>

Caption Analysis: The scene is a top-down view featuring:
A wooden table.
Two apples positioned on the table.

Bounding Boxes:
Wooden Table: [20, 148, 472, 216]
Positioned starting at x=20, y=148 with a width of 472 and a height of 216.
The table's coverage is extensive, suggesting it's the primary object in the scene.
First Apple: [150, 226, 100, 100]
Positioned starting at x=150, y=226 with a width and height of 100.
This square shape is appropriate for an apple in a top-down view.
Second Apple: [280, 226, 100, 100]
Positioned starting at x=280, y=226 with a width and height of 100.
Similar to the first apple, indicating consistency in depiction.

Analysis of Adherence:
Table Placement and Size:
The table occupies a significant portion of the scene, which is expected in a top-down view. Its large width (472) relative to its height (216) suggests a surface area large enough to hold objects, fitting the description of a wooden table.
Apples on the Table:
Both apples are placed with their top-left corners at y=226, which is within the table's y-range (148 to 364). This confirms they are on the table. Their x-coordinates (150 and 280) and sizes (100x100) ensure they are distinct objects on the table without overlapping, adhering to the realistic depiction.
Spatial Relationship Between Apples:
The apples are placed next to each other horizontally (as indicated by their x-coordinates and the absence of y-coordinate variance), which is an expected arrangement for objects on a table in a top-down view.

Conclusion:
The objects and their coordinates accurately adhere to the scene caption. The wooden table's size and placement provide a broad, realistic surface for the apples. The apples are depicted as distinct, non-overlapping objects on the table, positioned in a way that is logical for a top-down view. This setup effectively creates a realistic depiction of a wooden table with two apples on it, viewed from above.

<End Explanation>

<Scene Three Begin>
Caption: A realistic scene of three skiers standing in a line on the snow near a palm tree
Objects: [('a skier', [5, 152, 139, 168]), ('a skier', [278, 192, 121, 158]), ('a skier', [148, 173, 124, 155]), ('a palm tree', [404, 105, 103, 251])]
Background prompt: A realistic outdoor scene with snow
Negative prompt: 
<Scene Three End>

Why does Scene Three's layout have no overlapping and adhere to the caption's description of spatial relationships? Please provide an explanation.

<Begin Explanation>

Caption Analysis: The scene describes a realistic outdoor snowy landscape with the following details:
Three skiers standing in a line.
A palm tree is present near the skiers.
Given these details, we need to ensure the bounding boxes for these objects adhere to their described spatial relationships within an outdoor snowy scene.

Bounding Boxes:
First Skier: [5, 152, 139, 168]
Positioned starting at x=5, y=152 with a width of 139 and a height of 168.
Second Skier: [278, 192, 121, 158]
Positioned starting at x=278, y=192 with a width of 121 and a height of 158.
Third Skier: [148, 173, 124, 155]
Positioned starting at x=148, y=173 with a width of 124 and a height of 155.
Palm Tree: [404, 105, 103, 251]
Positioned starting at x=404, y=105 with a width of 103 and a height of 251.

Analysis of Adherence:
Skiers in a Line:
The skiers are positioned in a way that could represent a line, but the sequence based on their x-coordinates seems to be out of order for a straight line formation. The correct order should reflect their positions as increasing in x-values without overlapping, ideally with the first skier having the lowest x-value, followed by the third, and then the second based on their current coordinates. However, their current arrangement (first, third, and then second) does somewhat maintain a line but not in the straightest or most orderly manner.
Near a Palm Tree:
The palm tree, with its starting x-coordinate at 404, is positioned to the right of all skiers. This placement adheres to the scene description, implying that the palm tree is near the skiers but does not specify which side. Given the broad interpretation of "near," this condition is met.

Conclusion:
While the skiers are not perfectly aligned in a straight line according to their x-coordinates, they are positioned sequentially from left to right, which could be interpreted as standing "in a line" from a less strict perspective. The palm tree is correctly placed to the side of the skiers, which aligns with the description. Therefore, the objects and their coordinates largely adhere to the scene caption, capturing a realistic outdoor scene with snow, three skiers, and a palm tree, albeit with some flexibility in interpreting the exact positioning of the skiers in relation to each other.

<End Explanation>

Caption: {prompt}
Objects: 
"""

templatev0_7 = """You are an intelligent bounding box generator. I will provide you with a description of a photo, scene, or painting. Your task is to generate the bounding boxes for the objects mentioned in the description, along with a background prompt describing the scene. The images are of size 512x512. The top-left corner has coordinates [0, 0]. The bottom-right corner has coordinates [512, 512]. The bounding boxes should not overlap or go beyond the image boundaries. Each bounding box should be in the format of (object name, [top-left x coordinate, top-left y coordinate, box width, box height]) and should not include more than one object. 
To prevent overlap, for any two boxes (box1 and box2), the conditions (x1 + w1 <= x2) or (x2 + w2 <= x1) for the x-coordinates or (y1 + h1 <= y2) or (y2 + h2 <= y1) for the y-coordinates must be met.
Furthermore, if the description uses spatial keywords ('left', 'right', 'above', 'below'), the positioning of the bounding boxes must reflect these relationships accurately. This means adjusting the centroids of the boxes (cx1, cy1 for box1; cx2, cy2 for box2) so that: cx1 < cx2 if Object A is to the left of B; cx1 > cx2 if A is to the right of B; cy1 < cy2 if A is above B; and cy1 > cy2 if A is below B. Centroids are calculated as cx = x + w//2 and cy = y + h//2.
Objects defined within the bounding boxes should not be repeated in the scene's background description. Exclude any non-relevant or omitted objects from this background narrative. Use "A realistic scene" as the background prompt if no background is given in the prompt. If needed, you can make reasonable guesses. Please refer to the example below for the desired format.

<Scene One Begin>
Caption: A realistic image of landscape scene depicting a green car parking on the left of a blue truck, with a red air balloon and a bird in the sky
Objects: [('a green car', [21, 281, 211, 159]), ('a blue truck', [269, 283, 209, 160]), ('a red air balloon', [66, 8, 145, 135]), ('a bird', [296, 42, 143, 100])]
Background prompt: A realistic landscape scene
Negative prompt:
<Scene One End>

Why does Scene One's layout have no overlapping and adhere to the caption's description of spatial relationships? Please provide an explanation.

<Begin Explanation>

Bounding Boxes:
Green Car: [21, 281, 211, 159]
Positioned starting at x=21, y=281 with a width of 211 and a height of 159.
The car's centroid can be calculated as (x + w/2, y + h/2) = (126.5, 360.5).
Blue Truck: [269, 283, 209, 160]
Positioned starting at x=269, y=283 with a width of 209 and a height of 160.
The truck's centroid can be calculated as (373.5, 363).
Red Air Balloon: [66, 8, 145, 135]
Positioned starting at x=66, y=8 with a width of 145 and a height of 135.
The air balloon's centroid can be calculated as (138.5, 75.5).
Bird: [296, 42, 143, 100]
Positioned starting at x=296, y=42 with a width of 143 and a height of 100.
The bird's centroid can be calculated as (367.5, 92).

Analysis of Adherence:
Spatial Relationship Between Car and Truck:
The green car's centroid is at x=126.5, and the blue truck's centroid is at x=373.5. This means the green car is to the left of the blue truck, which adheres to the caption.
Objects in the Sky:
Both the red air balloon and the bird are positioned with low y-values (8 and 42, respectively), indicating they are in the sky, adhering to the caption's description.
Non-Overlapping and Within Boundaries:
The provided coordinates ensure that none of the bounding boxes overlap with one another, and all are within the 512x512 boundary.

<End Explanation>

<Scene Two Begin>
Caption: A realistic top-down view of a wooden table with two apples on it
Objects: [('a wooden table', [20, 148, 472, 216]), ('an apple', [150, 226, 100, 100]), ('an apple', [280, 226, 100, 100])]
Background prompt: A realistic top-down view
Negative prompt: 
<Scene Two End>

Why does Scene Two's layout have no overlapping and adhere to the caption's description of spatial relationships? Please provide an explanation.

<Begin Explanation>

Bounding Boxes:
Wooden Table: [20, 148, 472, 216]
Positioned starting at x=20, y=148 with a width of 472 and a height of 216.
The table's coverage is extensive, suggesting it's the primary object in the scene.
First Apple: [150, 226, 100, 100]
Positioned starting at x=150, y=226 with a width and height of 100.
This square shape is appropriate for an apple in a top-down view.
Second Apple: [280, 226, 100, 100]
Positioned starting at x=280, y=226 with a width and height of 100.
Similar to the first apple, indicating consistency in depiction.

Analysis of Adherence:
Table Placement and Size:
The table occupies a significant portion of the scene, which is expected in a top-down view. Its large width (472) relative to its height (216) suggests a surface area large enough to hold objects, fitting the description of a wooden table.
Apples on the Table:
Both apples are placed with their top-left corners at y=226, which is within the table's y-range (148 to 364). This confirms they are on the table. Their x-coordinates (150 and 280) and sizes (100x100) ensure they are distinct objects on the table without overlapping, adhering to the realistic depiction.
Spatial Relationship Between Apples:
The apples are placed next to each other horizontally (as indicated by their x-coordinates and the absence of y-coordinate variance), which is an expected arrangement for objects on a table in a top-down view.

<End Explanation>

<Scene Three Begin>
Caption: A realistic scene of three skiers standing in a line on the snow near a palm tree
Objects: [('a skier', [5, 152, 139, 168]), ('a skier', [278, 192, 121, 158]), ('a skier', [148, 173, 124, 155]), ('a palm tree', [404, 105, 103, 251])]
Background prompt: A realistic outdoor scene with snow
Negative prompt: 
<Scene Three End>

Why does Scene Three's layout have no overlapping and adhere to the caption's description of spatial relationships? Please provide an explanation.

<Begin Explanation>

Bounding Boxes:
First Skier: [5, 152, 139, 168]
Positioned starting at x=5, y=152 with a width of 139 and a height of 168.
Second Skier: [278, 192, 121, 158]
Positioned starting at x=278, y=192 with a width of 121 and a height of 158.
Third Skier: [148, 173, 124, 155]
Positioned starting at x=148, y=173 with a width of 124 and a height of 155.
Palm Tree: [404, 105, 103, 251]
Positioned starting at x=404, y=105 with a width of 103 and a height of 251.

Analysis of Adherence:
Skiers in a Line:
The skiers are positioned in a way that could represent a line, but the sequence based on their x-coordinates seems to be out of order for a straight line formation. The correct order should reflect their positions as increasing in x-values without overlapping, ideally with the first skier having the lowest x-value, followed by the third, and then the second based on their current coordinates. However, their current arrangement (first, third, and then second) does somewhat maintain a line but not in the straightest or most orderly manner.
Near a Palm Tree:
The palm tree, with its starting x-coordinate at 404, is positioned to the right of all skiers. This placement adheres to the scene description, implying that the palm tree is near the skiers but does not specify which side. Given the broad interpretation of "near," this condition is met.

<End Explanation>

Caption: {prompt}
Objects: 
"""


templatev0_8 = """You are an intelligent bounding box generator. I will provide you with a description of a photo, scene, or painting. Your task is to generate the bounding boxes for the objects mentioned in the description and a background prompt describing the scene. The images are of size 512x512. The top-left corner has coordinates [0, 0]. The bottom-right corner has coordinates [512, 512]. The bounding boxes should not overlap or go beyond the image boundaries. Each bounding box should be in the format of (object name, [top-left x coordinate, top-left y coordinate, box width, box height]) and should not include more than one object. 
To prevent overlap, for any two boxes (box1 and box2), the condition (x1 + w1 <= x2) or (x2 + w2 <= x1) or (y1 + h1 <= y2) or (y2 + h2 <= y1) must be met.
Furthermore, if the description uses spatial keywords ('left', 'right', 'above', 'below'), the positioning of the bounding boxes must reflect these relationships accurately. This means adjusting the centroids of the boxes (cx1, cy1 for box1; cx2, cy2 for box2) so that: cx1 < cx2 if Object A is to the left of B; cx1 > cx2 if A is to the right of B; cy1 < cy2 if A is above B; and cy1 > cy2 if A is below B. Centroids are calculated as cx = x + w//2 and cy = y + h//2.
Objects defined within the bounding boxes should not be repeated in the scene's background description. Exclude any non-relevant or omitted objects from this background narrative. Use "A realistic scene" as the background prompt if no background is given in the prompt. If needed, you can make reasonable guesses. Please refer to the example below for the desired format.

<Scene One Begin>
Caption: A realistic image of landscape scene depicting a green car parking on the left of a blue truck, with a red air balloon and a bird in the sky
Objects: [('a green car', [21, 281, 211, 159]), ('a blue truck', [269, 283, 209, 160]), ('a red air balloon', [66, 8, 145, 135]), ('a bird', [296, 42, 143, 100])]
Background prompt: A realistic landscape scene
Negative prompt:
<Scene One End>

Why does Scene One's layout have no overlapping and adhere to the caption's description of spatial relationships? Please provide an explanation.

<Begin Explanation>

Bounding Boxes:
Green Car: [21, 281, 211, 159]
Positioned starting at x=21, y=281 with a width of 211 and a height of 159.
The car's centroid can be calculated as (x + w/2, y + h/2) = (126.5, 360.5).
Blue Truck: [269, 283, 209, 160]
Positioned starting at x=269, y=283 with a width of 209 and a height of 160.
The truck's centroid can be calculated as (373.5, 363).
Red Air Balloon: [66, 8, 145, 135]
Positioned starting at x=66, y=8 with a width of 145 and a height of 135.
The air balloon's centroid can be calculated as (138.5, 75.5).
Bird: [296, 42, 143, 100]
Positioned starting at x=296, y=42 with a width of 143 and a height of 100.
The bird's centroid can be calculated as (367.5, 92).

Analysis of Adherence:
Spatial Relationship Between Car and Truck:
The green car's centroid is at x=126.5, and the blue truck's centroid is at x=373.5. This means the green car is to the left of the blue truck, which adheres to the caption.
Objects in the Sky:
Both the red air balloon and the bird are positioned with low y-values (8 and 42, respectively), indicating they are in the sky, adhering to the caption's description.
Non-Overlapping and Within Boundaries:
The provided coordinates ensure that none of the bounding boxes overlap with one another, and all are within the 512x512 boundary.

<End Explanation>

<Scene Two Begin>
Caption: A realistic top-down view of a wooden table with two apples on it
Objects: [('a wooden table', [20, 148, 472, 216]), ('an apple', [150, 226, 100, 100]), ('an apple', [280, 226, 100, 100])]
Background prompt: A realistic top-down view
Negative prompt: 
<Scene Two End>

Why does Scene Two's layout have no overlapping and adhere to the caption's description of spatial relationships? Please provide an explanation.

<Begin Explanation>

Bounding Boxes:
Wooden Table: [20, 148, 472, 216]
Positioned starting at x=20, y=148 with a width of 472 and a height of 216.
The table's coverage is extensive, suggesting it's the primary object in the scene.
First Apple: [150, 226, 100, 100]
Positioned starting at x=150, y=226 with a width and height of 100.
This square shape is appropriate for an apple in a top-down view.
Second Apple: [280, 226, 100, 100]
Positioned starting at x=280, y=226 with a width and height of 100.
Similar to the first apple, indicating consistency in depiction.

Analysis of Adherence:
Table Placement and Size:
The table occupies a significant portion of the scene, which is expected in a top-down view. Its large width (472) relative to its height (216) suggests a surface area large enough to hold objects, fitting the description of a wooden table.
Apples on the Table:
Both apples are placed with their top-left corners at y=226, which is within the table's y-range (148 to 364). This confirms they are on the table. Their x-coordinates (150 and 280) and sizes (100x100) ensure they are distinct objects on the table without overlapping, adhering to the realistic depiction.
Spatial Relationship Between Apples:
The apples are placed next to each other horizontally (as indicated by their x-coordinates and the absence of y-coordinate variance), which is an expected arrangement for objects on a table in a top-down view.

<End Explanation>

<Scene Three Begin>
Caption: A realistic scene of three skiers standing in a line on the snow near a palm tree
Objects: [('a skier', [5, 152, 139, 168]), ('a skier', [278, 192, 121, 158]), ('a skier', [148, 173, 124, 155]), ('a palm tree', [404, 105, 103, 251])]
Background prompt: A realistic outdoor scene with snow
Negative prompt: 
<Scene Three End>

Why does Scene Three's layout have no overlapping and adhere to the caption's description of spatial relationships? Please provide an explanation.

<Begin Explanation>

Bounding Boxes:
First Skier: [5, 152, 139, 168]
Positioned starting at x=5, y=152 with a width of 139 and a height of 168.
Second Skier: [278, 192, 121, 158]
Positioned starting at x=278, y=192 with a width of 121 and a height of 158.
Third Skier: [148, 173, 124, 155]
Positioned starting at x=148, y=173 with a width of 124 and a height of 155.
Palm Tree: [404, 105, 103, 251]
Positioned starting at x=404, y=105 with a width of 103 and a height of 251.

Analysis of Adherence:
Skiers in a Line:
The skiers are positioned in a way that could represent a line, but the sequence based on their x-coordinates seems to be out of order for a straight line formation. The correct order should reflect their positions as increasing in x-values without overlapping, ideally with the first skier having the lowest x-value, followed by the third, and then the second based on their current coordinates. However, their current arrangement (first, third, and then second) does somewhat maintain a line but not in the straightest or most orderly manner.
Near a Palm Tree:
The palm tree, with its starting x-coordinate at 404, is positioned to the right of all skiers. This placement adheres to the scene description, implying that the palm tree is near the skiers but does not specify which side. Given the broad interpretation of "near," this condition is met.

<End Explanation>

Caption: {prompt}
Objects: 
"""

templatev0_9 = """You are an intelligent bounding box generator. I will provide you with a description of a photo, scene, or painting. Your task is to generate the bounding boxes for the objects mentioned in the description and a background prompt describing the scene. The images are of size 512x512. The top-left corner has coordinates [0, 0]. The bottom-right corner has coordinates [512, 512]. The bounding boxes should not overlap or go beyond the image boundaries. Each bounding box should be in the format of (object name, [top-left x coordinate, top-left y coordinate, box width, box height]) and should not include more than one object. 
To prevent overlap, for any two boxes (box1 and box2), the condition (x1 + w1 <= x2) or (x2 + w2 <= x1) or (y1 + h1 <= y2) or (y2 + h2 <= y1) must be met.
Furthermore, if the description uses spatial keywords ('left', 'right', 'above', 'below'), the positioning of the bounding boxes must reflect these relationships accurately. This means adjusting the centroids of the boxes (cx1, cy1 for box1; cx2, cy2 for box2) so that: cx1 < cx2 if Object A is to the left of B; cx1 > cx2 if A is to the right of B; cy1 < cy2 if A is above B; and cy1 > cy2 if A is below B. Centroids are calculated as cx = x + w//2 and cy = y + h//2.
Objects defined within the bounding boxes should not be repeated in the scene's background description. Exclude any non-relevant or omitted objects from this background narrative. Use "A realistic scene" as the background prompt if no background is given in the prompt. If needed, you can make reasonable guesses. Please refer to the example below for the desired format.


<Scene One Begins>

Caption: A white background with 3 objects (['bicycle', 'boat', 'laptop']): the bicycle is below the boat; the boat is above the laptop.
Objects: [('bicycle', [150, 300, 200, 150]), ('boat', [150, 150, 200, 100]), ('laptop', [150, 50, 200, 75])]
Background prompt: A white background
Negative prompt: 

<Scene One Ends>

Why does Scene One's layout have no overlapping and adhere to the caption's description of spatial relationships? Please explain.

<Begin Explanation>

For every bounding box (x, y, w, h), max(x + w, y + h) < 512, so that every object is within the 512x512 size.
For every two boxes with coordinates (x1, y1, w1, h1) and (x2, y2, w2, h2), the condition (x1 + w1 <= x2) or (x2 + w2 <= x1) or (y1 + h1 <= y2) or (y2 + h2 <= y1) is met (e.g. for boxes of 'boat' and 'laptop, x2 + w2 = 150 + 200 = 350 <= 350 = x1), so there is no overlapping between each object.
For every two objects A, B with coordinates (xa, ya, wa, ha) and (xb, yb, wb, hb) and a spatial relationship Rel(A, B), their spatial relationship is met (e.g. for boxes of 'bicycle' and 'boat', the centroids for the bicycle is [150+200//2, 300+150//2] = [250, 375] and the centroid for the boat is [150+200//2, 150+100//2] = [250, 200]. Since Rel(bicycle, boat) is “below” and 375 > 200, the two objects have the correct spatial relationship as described).

<End Explanation>


<Scene Two Begins>

Caption: A white background with 4 objects (['elephant', 'toothbrush', 'microwave', 'handbag']): the elephant is below the toothbrush; the toothbrush is to the right of the microwave; the microwave is to the right of the handbag.
Objects: [('elephant', [150, 300, 200, 150]), ('toothbrush', [300, 150, 50, 150]), ('microwave', [200, 50, 100, 100]), ('handbag', [50, 50, 100, 100])]
Background prompt: A white background
Negative prompt:

<Scene Two Ends>

Why does Scene Two's layout have no overlapping and adhere to the caption's description of spatial relationships? Please explain.

<Begin Explanation>

For every bounding box (x, y, w, h), max(x + w, y + h) < 512, so that every object is within the 512x512 size.
For every two boxes with coordinates (x1, y1, w1, h1) and (x2, y2, w2, h2), the condition (x1 + w1 <= x2) or (x2 + w2 <= x1) or (y1 + h1 <= y2) or (y2 + h2 <= y1) is met (e.g. for boxes of 'elephant' and 'handbag', x2 + w2 = 50 + 100 = 150 <= 150 = x1), so there is no overlapping between each object.
For every two objects A, B with coordinates (xa, ya, wa, ha) and (xb, yb, wb, hb) and a spatial relationship Rel(A, B), their spatial relationship is met (e.g. for boxes of 'toothbrush' and 'microwave', the centroids for the toothbrush are [300+150//2, 150+150//2] = [375, 225] and the centroids for the microwave are [200+100//2, 50+100//2] = [250, 100]. Since Rel(toothbrush, microwave) is “right” and 225 > 100, the two objects have the correct spatial relationship as described).

<End Explanation>


<Scene Three Begins>

Caption: A white background with 5 objects (['stop sign', 'sink', 'clock', 'tennis racket', 'couch']): the stop sign is below the sink; the sink is to the left of the clock; the clock is below the tennis racket; the tennis racket is to the left of the couch.
Objects: [('stop sign', [150, 300, 80, 80]), ('sink', [150, 200, 80, 80]), ('clock', [250, 200, 80, 80]), ('tennis racket', [250, 100, 80, 80]), ('couch', [350, 100, 120, 80])]
Background prompt: A white background
Negative prompt:

<Scene Three Ends>

Why does Scene Three's layout have no overlapping and adhere to the caption's description of spatial relationships? Please explain.

<Begin Explanation>

For every bounding box (x, y, w, h), max(x + w, y + h) < 512, so that every object is within the 512x512 size.
For every two boxes with coordinates (x1, y1, w1, h1) and (x2, y2, w2, h2), the condition (x1 + w1 <= x2) or (x2 + w2 <= x1) or (y1 + h1 <= y2) or (y2 + h2 <= y1) is met (e.g. for boxes of 'clock' and 'couch', y2 + h2 = 100 + 80 = 180 <= 200 = y1), so there is no overlapping between each object.
For every two objects A, B with coordinates (xa, ya, wa, ha) and (xb, yb, wb, hb) and a spatial relationship Rel(A, B), their spatial relationship is met (e.g. for boxes of 'stop sign' and 'sink', the centroids for the stop sign is [150+80//2, 300+80//2] = [190, 340] and the centroid for the sink is [150+80//2, 200+80//2] = [190, 240]. Since Rel(stop sign, sink) is “below” and 340 > 240, the two objects have the correct spatial relationship as described).

<End Explanation>

Caption: {prompt}
Objects: 
"""


templatev0_10 = """You are an intelligent bounding box generator. I will provide you with a description of a photo, scene, or painting. Your task is to generate the bounding boxes for the objects mentioned in the description and a background prompt describing the scene. The images are of size 512x512. The top-left corner has coordinates [0, 0]. The bottom-right corner has coordinates [512, 512]. The bounding boxes should not overlap or go beyond the image boundaries. Each bounding box should be in the format of (object name, [top-left x coordinate, top-left y coordinate, box width, box height]) and should not include more than one object. 
To prevent overlap, for any two boxes (box1 and box2), the condition (x1 + w1 <= x2) or (x2 + w2 <= x1) or (y1 + h1 <= y2) or (y2 + h2 <= y1) must be met.
Furthermore, if the description uses spatial keywords ('left', 'right', 'above', 'below'), the positioning of the bounding boxes must reflect these relationships accurately. This means adjusting the centroids of the boxes (cx1, cy1 for box1; cx2, cy2 for box2) so that: cx1 < cx2 if Object A is to the left of B; cx1 > cx2 if A is to the right of B; cy1 < cy2 if A is above B; and cy1 > cy2 if A is below B. Centroids are calculated as cx = x + w//2 and cy = y + h//2.
Objects defined within the bounding boxes should not be repeated in the scene's background description. Exclude any non-relevant or omitted objects from this background narrative. Use "A realistic scene" as the background prompt if no background is given in the prompt. If needed, you can make reasonable guesses. Please refer to the example below for the desired format.


<Scene One Begins>

Caption: A white background with 3 objects (['bicycle', 'boat', 'laptop']): the bicycle is below the boat; the boat is above the laptop.
Objects: [('bicycle', [150, 300, 200, 150]), ('boat', [150, 150, 200, 100]), ('laptop', [150, 50, 200, 75])]
Background prompt: A white background
Negative prompt: 

<Scene One Ends>


<Begin Explanation>

Why does Scene One's layout have no overlapping and adhere to the caption's description of spatial relationships? Please explain.

For every bounding box (x, y, w, h), max(x + w, y + h) < 512, so that every object is within the 512x512 size.
For every two boxes with coordinates (x1, y1, w1, h1) and (x2, y2, w2, h2), the condition (x1 + w1 <= x2) or (x2 + w2 <= x1) or (y1 + h1 <= y2) or (y2 + h2 <= y1) is met (e.g. for boxes of 'boat' and 'laptop, x2 + w2 = 150 + 200 = 350 <= 350 = x1), so there is no overlapping between each object.
For every two objects A, B with coordinates (xa, ya, wa, ha) and (xb, yb, wb, hb) and a spatial relationship Rel(A, B), their spatial relationship is met (e.g. for boxes of 'bicycle' and 'boat', the centroids for the bicycle is [150+200//2, 300+150//2] = [250, 375] and the centroid for the boat is [150+200//2, 150+100//2] = [250, 200]. Since Rel(bicycle, boat) is “below” and 375 > 200, the two objects have the correct spatial relationship as described).

<End Explanation>


<Scene Two Begins>

Caption: A white background with 4 objects (['elephant', 'toothbrush', 'microwave', 'handbag']): the elephant is below the toothbrush; the toothbrush is to the right of the microwave; the microwave is to the right of the handbag.
Objects: [('elephant', [150, 300, 200, 150]), ('toothbrush', [300, 150, 50, 150]), ('microwave', [200, 50, 100, 100]), ('handbag', [50, 50, 100, 100])]
Background prompt: A white background
Negative prompt:

<Scene Two Ends>


<Begin Explanation>

Why does Scene Two's layout have no overlapping and adhere to the caption's description of spatial relationships? Please explain.

For every bounding box (x, y, w, h), max(x + w, y + h) < 512, so that every object is within the 512x512 size.
For every two boxes with coordinates (x1, y1, w1, h1) and (x2, y2, w2, h2), the condition (x1 + w1 <= x2) or (x2 + w2 <= x1) or (y1 + h1 <= y2) or (y2 + h2 <= y1) is met (e.g. for boxes of 'elephant' and 'handbag', x2 + w2 = 50 + 100 = 150 <= 150 = x1), so there is no overlapping between each object.
For every two objects A, B with coordinates (xa, ya, wa, ha) and (xb, yb, wb, hb) and a spatial relationship Rel(A, B), their spatial relationship is met (e.g. for boxes of 'toothbrush' and 'microwave', the centroids for the toothbrush are [300+150//2, 150+150//2] = [375, 225] and the centroids for the microwave are [200+100//2, 50+100//2] = [250, 100]. Since Rel(toothbrush, microwave) is “right” and 225 > 100, the two objects have the correct spatial relationship as described).

<End Explanation>


<Scene Three Begins>

Caption: A white background with 5 objects (['stop sign', 'sink', 'clock', 'tennis racket', 'couch']): the stop sign is below the sink; the sink is to the left of the clock; the clock is below the tennis racket; the tennis racket is to the left of the couch.
Objects: [('stop sign', [150, 300, 80, 80]), ('sink', [150, 200, 80, 80]), ('clock', [250, 200, 80, 80]), ('tennis racket', [250, 100, 80, 80]), ('couch', [350, 100, 120, 80])]
Background prompt: A white background
Negative prompt:

<Scene Three Ends>


<Begin Explanation>

Why does Scene Three's layout have no overlapping and adhere to the caption's description of spatial relationships? Please explain.

For every bounding box (x, y, w, h), max(x + w, y + h) < 512, so that every object is within the 512x512 size.
For every two boxes with coordinates (x1, y1, w1, h1) and (x2, y2, w2, h2), the condition (x1 + w1 <= x2) or (x2 + w2 <= x1) or (y1 + h1 <= y2) or (y2 + h2 <= y1) is met (e.g. for boxes of 'clock' and 'couch', y2 + h2 = 100 + 80 = 180 <= 200 = y1), so there is no overlapping between each object.
For every two objects A, B with coordinates (xa, ya, wa, ha) and (xb, yb, wb, hb) and a spatial relationship Rel(A, B), their spatial relationship is met (e.g. for boxes of 'stop sign' and 'sink', the centroids for the stop sign is [150+80//2, 300+80//2] = [190, 340] and the centroid for the sink is [150+80//2, 200+80//2] = [190, 240]. Since Rel(stop sign, sink) is “below” and 340 > 240, the two objects have the correct spatial relationship as described).

<End Explanation>

Caption: {prompt}
Objects: 
"""




DEFAULT_SO_NEGATIVE_PROMPT = "artifacts, blurry, smooth texture, bad quality, distortions, unrealistic, distorted image, bad proportions, duplicate, two, many, group, occlusion, occluded, side, border, collate"
DEFAULT_OVERALL_NEGATIVE_PROMPT = "artifacts, blurry, smooth texture, bad quality, distortions, unrealistic, distorted image, bad proportions, duplicate"

templates = {"v0.1": templatev0_1, "v0.2": templatev0_2, "v0.3": templatev0_3, "v0.4": templatev0_4, "v0.5": templatev0_5, "v0.6": templatev0_6, "v0.7": templatev0_7, "v0.8": templatev0_8, "v0.9": templatev0_9, "v0.10": templatev0_10}
template_versions = ["v0.1", "v0.2", "v0.3", "v0.4", "v0.5", "v0.6", "v0.7", "v0.8", "v0.9", "v0.10"]

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


    "In a bustling downtown area during evening rush, a person leans against a streetlight, waiting to cross the road. Nearby, a parked motorcycle reflects the fading light, while a city bus halts at a designated stop. Across the street, a bicycle is securely locked to a bike rack, and a stray cat watches the busy scene from a safe distance.",
"Along a peaceful riverbank, a couple (two people) relax on a bench, enjoying the view. A carefully parked bicycle leans against a nearby tree. A playful dog runs around, occasionally chasing birds that land near the water's edge. In the background, a boat slowly cruises down the river.",
"In a suburban neighborhood, a person jogs past a row of houses, each with a car in the driveway. At a nearby house, a dog barks from the yard, drawing the attention of a bird perched on the mailbox. On the sidewalk, a child's abandoned bicycle lies next to a fire hydrant.",
"A lively city park scene where a person reads a book on a bench under a tree. Nearby, a mother and child (two people) play frisbee on the grass. A curious squirrel (animal) scampers around, occasionally stopping to observe. In the distance, a parked motorcycle and a bicycle stand by a park entrance.",
"On a rustic farmstead, a person feeds chickens near a barn. A few sheep graze in an adjacent paddock, while a horse stands by the fence, watching a passing train in the distance. Near the farmhouse, a truck is parked, with its headlights reflecting off a nearby water trough."
"A serene park scene with a bench, a bicycle leaning against a nearby tree, a playful dog chasing a frisbee, and a distant cat observing from atop a wall.",
"A bustling city street featuring a car waiting at a traffic light, a bus passing by, a pedestrian carrying an umbrella, and a taxi parked by a fire hydrant.",
"A cozy living room with a couch, a coffee table holding a remote and a cup, a tv on a stand, and a cat sleeping on a nearby rug."

'A park scene with a bench, a bicycle leaning against a tree, a person reading a book, a dog sitting beside them, and a frisbee lying on the grass nearby.',
 'A busy city street with a car stopped at a traffic light, a bus in the next lane, a pedestrian waiting to cross, a motorcycle weaving through traffic, and a taxi parked by the sidewalk.',
 'A beach scene where a person is lying on a towel, a surfboard stuck in the sand, a kite flying in the sky, a cooler with a bottle poking out, and a pair of flip-flops tossed aside.',
 'A cozy living room with a couch, a coffee table with a vase of flowers, a cat sleeping in a sunbeam, a television displaying a nature documentary, and a bookshelf filled with books.',
 'A train station with a train pulling into the platform, a person holding a suitcase, a bench with a backpack resting on it, a vending machine dispensing bottles, and a clock showing the time.',
 "A farmer's market scene with a stand selling apples and oranges, a person carrying a handbag and selecting a carrot, a vendor handing over a bunch of bananas, a dog tied to a post, and a bench for resting.",
 'An airport lounge with a person typing on a laptop, a suitcase by their side, a cup of coffee on the table, a flight information board displaying times, and a window showing airplanes on the runway.',
 'A public library with rows of bookshelves, a person browsing a book, a chair and table with a laptop and a mouse, a clock on the wall, and a librarian scanning books at the checkout desk.',
 'A nighttime camping scene with a tent, a campfire casting shadows, a person roasting a hot dog on a stick, a backpack leaning against a tree, and a flashlight illuminating a map.',
 'A home office setup with a desk, a chair, a laptop open and running, a cup holding pens and pencils, a potted plant on the windowsill, and a cell phone charging beside the computer.',
 'A birthday party scene with a table covered in a cloth, a cake with candles lit, a bunch of balloons tied to the chair, a person wearing a party hat, and a pile of presents wrapped in colorful paper.',
 'A picnic in the park with a blanket spread on the grass, a basket containing a loaf of bread and a bottle of wine, a person lying down reading a book, a bicycle parked nearby, and a dog chasing a ball.',
 'A home kitchen scene with a person cooking, a pot on the stove, a knife and cutting board with vegetables, a bowl of fruit on the counter, and an oven preheating for baking.',
 'A street artist setting with a person painting on a canvas, a bench serving as a makeshift table for paint supplies, a crowd watching, a dog sitting patiently, and a hat on the ground for tips.',
 'A morning jog in a city park with a person running, a bench where a water bottle and a towel rest, a dog playing with a frisbee, a bicycle passing by, and a squirrel watching curiously.',
 'A snowy day scene with a person wearing a backpack and holding a snowboard, a bench covered in snow, a dog wearing a coat, a snowman with a carrot nose, and a hot chocolate stand with a queue.',
 'A luxury yacht scene with a boat anchored near the shore, a person sunbathing on the deck, a bottle of champagne chilling, a pair of sunglasses on a table, and a seagull perched on the railing.',
 'An outdoor barbecue with a person grilling burgers, a table set with plates and forks, a dog waiting hopefully, a cooler with bottles of soda, and a kite stuck in a nearby tree.',
 'A college campus scene with a student sitting on a bench reading a book, a bicycle parked in a rack, a squirrel darting past, a backpack resting against the bench, and a frisbee lying on the grass.',
 'A romantic evening setup with a table for two, a vase with a single rose, two wine glasses ready to be filled, a person lighting a candle, and a guitar resting against the chair ready for serenading.',
 'A city bus stop with a person waiting, a bus approaching, a bicycle locked to a nearby post, a stray cat lounging in the sun, and a poster advertising a local event.',
 'A farm scene with a person feeding a sheep, a dog herding cows in the distance, a tractor parked by the barn, a pile of hay bales, and a horse peeking over the fence.',
 "A zoo visit with a family watching an elephant, a child holding a balloon, a bench where a backpack and a camera rest, a vendor selling ice cream, and a map of the zoo in a person's hand.",
 'A mountain hiking trail with a person wearing a backpack, a sign pointing to the summit, a dog trotting ahead, a clear stream crossing the path, and a bird perched on a nearby tree.',
 'A street food festival with a person holding a plate of tacos, a vendor cooking pizza in a portable oven, a dog waiting for scraps, a group of people sitting on benches eating, and a musician playing a guitar.',
 'A school playground with children playing on swings, a teacher supervising from a bench, a backpack lying on the ground, a ball bouncing away, and a bicycle parked against the fence.',
 'A winter ski resort scene with a person carrying skis, a snowboard propped against a lodge, a dog wearing a small sweater, a hot cocoa stand, and a fire pit with chairs around it.',
 'A garden party with a table set with a vase of flowers, a person carrying a tray of sandwiches, a dog lounging under the table, a guitar leaning against a chair, and lanterns hanging from the trees.',
 'A garage sale with a table displaying books and toys, a person examining a vase, a dog tied to a post, a sign advertising the sale, and a box of free items marked "Take Me."',
 "A cozy reading nook with a chair, a lamp casting a warm light, a book open on a person's lap, a cup of tea on a nearby table, and a cat curled up beside the reader.",
 'An art gallery opening with paintings hanging on the walls, a person admiring a sculpture, a table with wine glasses and a bottle, a book of guest signatures, and an artist discussing their work.',
 'A city rooftop garden with potted plants, a person practicing yoga, a dog watching pigeons, a bench with a book and sunglasses, and a water bottle resting beside a mat.',
 'A horseback riding trail with a person on a horse, a dog running alongside, a bench for resting, a water bottle tied to the saddle, and a bird flying overhead.',
 'A vintage car show with a row of classic cars, a person polishing a shiny bumper, a dog sitting in the shade, a cooler with refreshments, and a sign announcing the event.',
 'A riverside picnic with a blanket spread out, a basket with a loaf of bread poking out, a person sketching the view, a dog splashing in the water, and a boat passing by.',
 'A backyard camping scene with a tent set up, a person roasting marshmallows over a fire pit, a dog curled up nearby, a flashlight illuminating a book, and a guitar waiting for a campfire song.',
 'A luxury hotel lobby with a person checking in, a bellhop carrying a suitcase, a couch where a cat is napping, a vase of fresh flowers on the reception desk, and a chandelier casting light.',
 'A bakery with a display of cakes and donuts, a person pointing at their choice, a dog waiting outside, a baker removing bread from the oven, and a vase with a single flower on the counter.',
 'A home gym setup with a person lifting weights, a yoga mat rolled up in the corner, a bottle of water on a table, a towel hanging over a chair, and a dog watching curiously.',
 'A vintage bookstore with shelves of books, a person browsing titles, a cat lounging on a windowsill, a clock ticking away, and a sign indicating a reading nook.',
 'A music studio with a person playing a keyboard, a guitar resting on a stand, a microphone set up for singing, a laptop recording the session, and a dog lying on a couch listening.',
 'An outdoor cinema night with a screen showing a film, a person sitting on a blanket with popcorn, a dog lying beside them, a bottle of soda, and a speaker providing sound.',
 'A skatepark with a person performing a trick on a skateboard, a dog watching from the sidelines, a bench where backpacks and helmets are piled, a bottle of water resting on the ground, and a graffiti-covered wall.',
 'A desert camping scene with a tent pitched on the sand, a person sitting on a folding chair watching the sunset, a dog digging in the sand, a cooler keeping drinks cold, and a flashlight ready for the night.',
 'A botanical garden tour with a guide pointing out flowers, a person taking photos with a cell phone, a bench for resting, a dog on a leash sniffing the plants, and a fountain bubbling in the background.',
 'A home cooking class with a person instructing on kneading dough, a table set with bowls and flour, a dog waiting for spills, a book of recipes open for reference, and a timer ticking down.',
 'A city rooftop party with a person DJing, a table with bottles and cups, a dog lounging under a chair, a cooler glowing with lights, and a view of the skyline at night.',
 'A forest hiking path with a person carrying a backpack, a sign marking the trail, a dog chasing butterflies, a bench overlooking a vista, and a bird singing from a tree.',
 'A riverside fishing trip with a person casting a line, a cooler for the catch, a dog watching the water, a bench for taking breaks, and a hat protecting from the sun.',
 'An urban garden project with a person planting seeds, a watering can ready for use, a dog digging beside, a bench made from recycled materials, and a sign welcoming volunteers.',
 'A winter cabin scene with a person sipping hot cocoa, a dog curled up by the fire, a pair of skis leaning against the wall, a book open on the couch, and a window showing falling snow.',
 'A neighborhood block party with a grill cooking hot dogs, a table with a cake and donut for dessert, a person leading a dance, a dog weaving through the crowd, and a banner announcing the event.',
 'A bird-watching expedition in a forest with a person using binoculars, a dog sitting quietly, a guidebook on birds resting on a log, a water bottle for hydration, and a bird singing overhead.',
 'A cityscape photography outing with a person setting up a tripod, a camera focusing on the skyline, a backpack with extra lenses, a dog posing for a test shot, and a sunset illuminating the buildings.'
]

# Put what we want to generate when you query GPT-3.5 for demo here
prompts_demo_gpt3_5 = []

prompt_types = [
    "demo",
    # "lmd_negation",
    "lmd_numeracy",
    # "lmd_attribution",
    "lmd_spatial",
    "lmd_complex",
    "lmd",
    "lmd_complex_50",
]


def get_prompts(prompt_type, model, allow_non_exist=False):
    """
    This function returns the text prompts according to the requested `prompt_type` and `model`. Set `model` to "all" to return all the text prompts in the current type. Otherwise we may want to have different prompts for gpt-3.5 and gpt-4 to prevent confusion.
    """
    prompts_gpt4, prompts_gpt3_5 = {}, {}
    if prompt_type.startswith("lmd"):
        # from utils.eval.lmd import get_lmd_prompts

        # prompts = get_lmd_prompts()

        # import json
        # import numpy as np
        # data = json.load(open("data/text_spatial_rel_phrases.json"))
        # all_spatial_rel_phrases = {'above', 'below', 'to the left of', 'to the right of'}
        # two_objs_data = []
        # two_objs_data_above = []
        # two_objs_data_below = []
        # two_objs_data_left = []
        # two_objs_data_right = []
        # for d in data:
        #     if d['rel_type'] in all_spatial_rel_phrases:
        #         two_objs_data.append(d)
        #         if d['rel_type'] == 'above':
        #             two_objs_data_above.append(d)
        #         elif d['rel_type'] == 'below':
        #             two_objs_data_below.append(d)
        #         elif d['rel_type'] == 'to the left of':
        #             two_objs_data_left.append(d)
        #         elif d['rel_type'] == 'to the right of':
        #             two_objs_data_right.append(d)
        # np.random.seed(0)
        # samples_below = np.random.choice(two_objs_data_below, 100, replace=False)
        # samples_above = np.random.choice(two_objs_data_above, 100, replace=False)
        # samples_left = np.random.choice(two_objs_data_left, 100, replace=False)
        # samples_right = np.random.choice(two_objs_data_right, 100, replace=False)
        # samples = list(np.concatenate([samples_below, samples_above, samples_left, samples_right]))
        if prompt_type == "lmd_spatial":
            import json
            samples = json.load(open("data/new_sample_3.json"))
            prompts = {'lmd_spatial': [d['text'] for d in samples]}
        elif prompt_type == "lmd_numeracy":
            import json
            samples = json.load(open("data/numeracy.json"))
            prompts = {'lmd_numeracy': [d['prompt'] for d in samples]}
        elif prompt_type == "lmd_complex":
            import json
            samples = json.load(open("data/complex_prompt.json"))
            prompts = {'lmd_complex': [d['text'] for d in samples]}
        elif prompt_type == "lmd_complex_50":
            import json
            samples = json.load(open("data/complex_prompt_50.json"))
            prompts = {'lmd_complex_50': [d['text'] for d in samples]}
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