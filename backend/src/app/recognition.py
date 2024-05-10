import torch
import cv2
import tqdm
from PIL import Image

from mappings import OBJECT_MAPPING, LABEL_MAPPING

object_recognition_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def filter_objects(image_path, boxed_items, threshold=0.3):
    """
    Filter boxed items to only include images of tables, chairs, beds, and couches
    Use YOLOv5 object recognition to ensure that the images contain the furniture as expected
    """

    full_image = Image.open(image_path)

    filtered_boxes = {}
    for item, boxes in tqdm.tqdm(boxed_items.items(), desc="Filtering boxes"):

        # Filter out items of furniture that is not desired (i.e. walls, windows, TVs, etc.)
        if item not in LABEL_MAPPING:
            continue

        new_boxes = []
        for _, bounding_box in enumerate(boxes):
            # Extract the crop from the image using the bounding box
            crop = full_image.crop(bounding_box)

            # Perform object detection on the image
            results = object_recognition_model(crop)
            class_labels = results.xyxy[0][:, 5]
            confidence_scores = results.xyxy[0][:, 4]
            outputs = zip(class_labels.tolist(), confidence_scores.tolist())

            # Iterate through results to validate image
            valid = False
            for output in outputs:
                class_num = output[0]
                confidence = output[1]

                # Filter out all objects that are not in OBJECT_MAPPING
                if not class_num in OBJECT_MAPPING:
                    continue
                
                label = OBJECT_MAPPING[class_num]
                if LABEL_MAPPING[item] != label:
                    continue

                # Filter out all images that do not actually contain the furniture as expected
                if confidence < threshold:
                    continue
                
                valid = True

            if valid:
                new_boxes.append(bounding_box)

        if len(new_boxes) > 0:
            filtered_boxes[item] = new_boxes

    return filtered_boxes