# python evaluate_images.py --template_version v0.1 --yolo_model yolov8m
# python evaluate_images.py --template_version v0.4 --yolo_model yolov8m
# python evaluate_images.py --template_version v0.7 --yolo_model yolov8m
# python evaluate_images.py --template_version v0.9 --yolo_model yolov8m

# python evaluate_images.py --template_version v0.1 --yolo_model yolov8x
# python evaluate_images.py --template_version v0.4 --yolo_model yolov8x
# python evaluate_images.py --template_version v0.7 --yolo_model yolov8x
# python evaluate_images.py --template_version v0.9 --yolo_model yolov8x


# python evaluate_images.py --template_version v0.1 --yolo_model yolov9e
# python evaluate_images.py --template_version v0.4 --yolo_model yolov9e
# python evaluate_images.py --template_version v0.7 --yolo_model yolov9e
# python evaluate_images.py --template_version v0.9 --yolo_model yolov9e


python evaluate_images.py --model_type tokencompose --yolo_model yolov8m
python evaluate_images.py --model_type tokencompose --yolo_model yolov8x
python evaluate_images.py --model_type tokencompose --yolo_model yolov9e


python evaluate_images.py --model_type sdxl --yolo_model yolov8m
python evaluate_images.py --model_type sdxl --yolo_model yolov8x
python evaluate_images.py --model_type sdxl --yolo_model yolov9e


