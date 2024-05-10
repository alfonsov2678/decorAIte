import numpy as np
import torch
import tqdm
import cv2
import json
from pathlib import Path
from PIL import Image
from transformers import AutoImageProcessor, UperNetForSemanticSegmentation
from diffusers.utils import load_image

from colors import COLOR_MAPPING_, palette


image_processor = AutoImageProcessor.from_pretrained("openmmlab/upernet-convnext-small")
image_segmentor = UperNetForSemanticSegmentation.from_pretrained("openmmlab/upernet-convnext-small")


def get_segmentation_boxes(image_path, save_to_disk=False):
    segmented_image, mask = segment_image(image_path)

    # Save segmented image to disk
    if save_to_disk:
        image_name = Path(image_path).stem
        segmented_image.save(f'segmented_images/segmented_{image_name}.png')

    boxed_items = {}
    for hex, item in tqdm.tqdm(COLOR_MAPPING_.items(), desc="Extracting boxes"):
        rgb = hex_to_rgb(hex)
        segmentation = np.all(mask == rgb, axis=-1)
        if segmentation.any():
            binary_mask = segmentation.astype(np.uint8)
            # Find contours in the binary mask
            contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # Initialize a list to store bounding boxes
            bounding_boxes = []
            # Iterate through each contour and compute the bounding box
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                bounding_boxes.append((x, y, x + w, y + h))  # Format: (x_min, y_min, x_max, y_max)
            # Filter bounding boxes with threshold = 0.15
            bounding_boxes = filter_boxes(bounding_boxes, 0.15)
            # Save to dictionary
            boxed_items[item] = torch.tensor(bounding_boxes)

    # Save boxed images to disk
    if save_to_disk:
        save_boxed_images(image_path, boxed_items)

    serialized_items = {key: value.tolist() for key, value in boxed_items.items()}

    # Save dictionary of boxed items to disk
    if save_to_disk:
        with open(f"extracted_images/{image_name}/item_boxes.json", "w") as json_file:
            json.dump(serialized_items, json_file)

    return serialized_items


def save_boxed_images(image_path, boxed_items):
    og_image = cv2.imread(image_path)
    image_name = Path(image_path).stem

    parent_directory = f'extracted_images/{image_name}'
    Path(parent_directory).mkdir(parents=True, exist_ok=True)

    for item, boxes in tqdm.tqdm(boxed_items.items()):
        Path(f'{parent_directory}/{item}').mkdir(exist_ok=True)
        for i, bounding_box in enumerate(boxes):
            # Extract the crop from the image using the bounding box coordinates
            crop = og_image[bounding_box[1]:bounding_box[3], bounding_box[0]:bounding_box[2]]
            key_str = '{}_{}.jpg'.format(item, i)
            cv2.imwrite(f'{parent_directory}/{item}/{key_str}', crop)


def segment_image(image_path):
    image = load_image(image_path).convert('RGB')

    pixel_values = image_processor(image, return_tensors="pt").pixel_values

    with torch.no_grad():
        outputs = image_segmentor(pixel_values)

    seg = image_processor.post_process_semantic_segmentation(outputs, target_sizes=[image.size[::-1]])[0]

    color_seg = np.zeros((seg.shape[0], seg.shape[1], 3), dtype=np.uint8) # height, width, 3

    for label, color in enumerate(palette):
        color_seg[seg == label, :] = color

    color_seg = color_seg.astype(np.uint8)

    image = Image.fromarray(color_seg).convert("RGB")

    return image, color_seg


# Helper functions 

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def hex_to_rgb(hex_code):
    # Remove '#' if present
    hex_code = hex_code.lstrip('#')

    # Extract individual color components
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)

    return r, g, b

def filter_boxes(boxes, threshold=0.75):
  """
  Filters by size to ensure tiny boxes are filtered out
  """

  # Calculate the area of each rectangle
  areas = [(rect[2] - rect[0]) * (rect[3] - rect[1]) for rect in boxes]

  # Find the area of the biggest rectangle
  max_area = max(areas)

  # Filter the list to include only rectangles with at least 75% of the area of the biggest rectangle
  filtered_boxes = [rect for rect, area in zip(boxes, areas) if area >= threshold * max_area]

  return filtered_boxes