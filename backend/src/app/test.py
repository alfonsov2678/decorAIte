from segmentation import get_segmentation_boxes
from composition import compose_image
from recognition import filter_objects

INPUT_IMAGE_PATH = "image-2.png"

if __name__ == "__main__":
    
   # BEFORE: CALL CONTROLNET API TO ADD THE IMAGE

   # NOW: EXTRACT THE BOUNDING BOXES FROM IMAGE
   boxes = get_segmentation_boxes(INPUT_IMAGE_PATH)
   # FILTER BOUNDING BOXES VIA OBJECT RECOGNITION
   boxes = filter_objects(INPUT_IMAGE_PATH, boxes)
   print(boxes)

   # TODO: ITERATE THROUGH BOUNDING BOXES, IN THIS EXAMPLE WE JUST USE ONE
   box = boxes['sofa;couch;lounge'][0]

   # TODO: CALL SIMILARITY PIPELINE TO RETURN MOST SIMILAR PRODUCT ID

   # COMPOSE IMAGE GIVEN PRODUCT ID (IN THIS EXAMPLE, WE USE COUCH5)
   compose_image(INPUT_IMAGE_PATH,
                 box,
                "couch",
                "couch5",
                5)
    # RESULTS WILL BE SAVED TO COMPOSED_IMAGES/ DIRECTORY
