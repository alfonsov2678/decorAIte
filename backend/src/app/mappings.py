# Map YOLOv5 model classes to our desired furniture items
OBJECT_MAPPING = {
    60: "table",
    56: "chair",
    59: "bed",
    57: "couch"
}

# Map segmentation labels to our desired furniture items
LABEL_MAPPING = {
    "coffee;table;cocktail;table": "table",
    "table": "table",
    "sofa;couch;lounge": "couch",
    "chair": "chair",
    "armchair": "chair",
    "swivel;chair": "chair",
    "bed": "bed"
}