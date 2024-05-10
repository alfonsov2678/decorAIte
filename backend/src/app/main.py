from fastapi import FastAPI
from PIL import Image

from similarity import find_product_similarity
from generation import generate_image
from segmentation import get_segmentation_boxes
from composition import compose_image
from recognition import filter_objects

app = FastAPI()

INPUT_IMAGE_PATH = "input_images/room5.jpg"

@app.get("/")
async def root():
    # Call ControlNet API to generate the image
    image_path = generate_image(INPUT_IMAGE_PATH, "“Stylish living room embracing mid-century modern aesthetic”")

    # Extract the bounding boxes from the image
    boxes = get_segmentation_boxes(image_path, save_to_disk=True)
    # Filter the bounding boxes via object recogntiion
    boxes = filter_objects(image_path, boxes, threshold=0.2)
    print(boxes)

    for item in boxes:
        for box in item:
            # Call similarity pipeline to return most similar product ID
            full_image = Image.open(image_path)
            crop_image = full_image.crop(box)
            result = find_product_similarity(crop_image)
            
            class_name = result['metadata']['class_name']
            product_id = result['metadata']['id']

            # Iteratively compose image with each product
            _, image_path = compose_image(image_path,
                                        box,
                                        class_name,
                                        product_id,
                                        5)
    return {"message": "Completed image composition"}