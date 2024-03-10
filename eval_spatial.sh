# python evaluate_images.py --template_version v0.1 --yolo_model yolov8m --lm gpt-3.5 #--detection True
# python evaluate_images.py --template_version v0.4 --yolo_model yolov8m --lm gpt-3.5 #--detection True
# python evaluate_images.py --template_version v0.7 --yolo_model yolov8m
# python evaluate_images.py --template_version v0.9 --yolo_model yolov8m

# python evaluate_images.py --template_version v0.1 --yolo_model yolov8x --lm gpt-3.5 #--detection True
# python evaluate_images.py --template_version v0.4 --yolo_model yolov8x --lm gpt-3.5 #--detection True
# python evaluate_images.py --template_version v0.7 --yolo_model yolov8x
# python evaluate_images.py --template_version v0.9 --yolo_model yolov8x


# python evaluate_images.py --template_version v0.1 --yolo_model yolov9e --lm gpt-3.5 #--detection True
# python evaluate_images.py --template_version v0.4 --yolo_model yolov9e --lm gpt-3.5 #--detection True
# python evaluate_images.py --template_version v0.7 --yolo_model yolov9e
# python evaluate_images.py --template_version v0.9 --yolo_model yolov9e


# python evaluate_images.py --model_type tokencompose --yolo_model yolov8m
# python evaluate_images.py --model_type tokencompose --yolo_model yolov8x
# python evaluate_images.py --model_type tokencompose --yolo_model yolov9e


# python evaluate_images.py --model_type sdxl --yolo_model yolov8m
# python evaluate_images.py --model_type sdxl --yolo_model yolov8x
# python evaluate_images.py --model_type sdxl --yolo_model yolov9e

# python evaluate_images.py --sdxl True --prompt_type lmd_spatial --template_version v0.1 --yolo_model yolov8m --lm gpt-4 --task spatial
# python evaluate_images.py --sdxl True --prompt_type lmd_spatial --template_version v0.7 --yolo_model yolov8m --lm gpt-4 --task spatial

# gligen
# python evaluate_images.py --prompt_type lmd_spatial --template_version v0.7 --yolo_model yolov8m --lm gpt-4 --task spatial

# python evaluate_images.py --prompt_type lmd_numeracy --template_version v0.7 --yolo_model yolov8m --lm gpt-4 --task numeracy --detection True

# python evaluate_images.py --prompt_type lmd_complex --template_version v0.7 --yolo_model yolov8m --lm gpt-4 --task complex --detection True


python evaluate_images.py --prompt_type lmd_complex --yolo_model yolov8m --lm gpt-4 --task complex --model_type sdxl --detection True
python evaluate_images.py --prompt_type lmd_complex --yolo_model yolov8m --lm gpt-4 --task complex --model_type tokencompose --detection True


# python evaluate_images.py --prompt_type lmd_complex --template_version v0.1 --yolo_model yolov8m --lm gpt-4 --task complex --sdxl True
# python evaluate_images.py --prompt_type lmd_complex --template_version v0.7 --yolo_model yolov8m --lm gpt-4 --task complex --sdxl True
# python evaluate_images.py --prompt_type lmd_complex --template_version v0.1 --yolo_model yolov8m --lm gpt-3.5 --task complex --sdxl True
# python evaluate_images.py --prompt_type lmd_complex --template_version v0.4 --yolo_model yolov8m --lm gpt-3.5 --task complex --sdxl True

