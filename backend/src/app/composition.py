import torch
import numpy as np
import random
import os

from pathlib import Path
from diffusers import StableDiffusionInpaintPipeline
import PIL.Image as Image

device = "cuda"
random.seed(666)
torch.manual_seed(666)

def compose_image(image_path, bbox, class_name, product_name, image_num):
    """
    Calls DreamCom Image Composition model to compose product image inside the base image
    image_path: Path to input image of fully decorated room
    bbox: x_min, y_min, x_max, y_max coordinates of where to place product inside base image
    class_name: Type of product (i.e. couch, desk, table)
    product_name: Name of product to insert within image, used to query DreamCom model fine-tuned on that product
    image_num: Number of images to generate for that product (must correspond to model name)
    """

    model_path = 'models/' + product_name + str(image_num)

    pipeline = StableDiffusionInpaintPipeline.from_pretrained(
                    model_path,
                    torch_dtype=torch.float16,
                    requires_safety_checker=False,
                    safety_checker=None)

    pipeline = pipeline.to(device)

    # Open image
    input_image = Image.open(image_path)

    # Make save directory 
    image_name = Path(image_path).stem
    box_id = "{}_{}_{}_{}".format(*bbox)
    save_path = f"tmp/composed_images/{image_name}/{product_name}/{box_id}"
    os.makedirs(save_path, exist_ok=True)

    x_left, y_bottom, x_right, y_top = bbox[0], bbox[1], bbox[2], bbox[3]
    W, H = (np.array(input_image)).shape[:2]
    mask_array_new = np.zeros((W, H))
    y_top = min(y_top, W - 1)
    x_right = min(x_right, H - 1)

    new_temp = np.ones((y_top - y_bottom + 1, x_right - x_left + 1)) * 255
    mask_array_new[y_bottom:y_top + 1, x_left:x_right + 1] = new_temp
    mask_array_new = np.uint8(mask_array_new)
    mask_image = Image.fromarray(mask_array_new)

    mask_W=y_top - y_bottom + 1
    mask_H=x_right - x_left + 1

    prompt = "a photo of sks " + class_name

    if mask_W*mask_H*4<W*H:

        scale=0.5
    
        y_bottom=max(0,y_bottom-int(scale*mask_W))
        x_left=max(0,x_left-int(scale*mask_H))
        y_top=min(W-1,y_top+int(scale*mask_W))
        x_right=min(H-1,x_right+int(scale*mask_H))

        new_W=y_top-y_bottom+1
        new_H=x_right-x_left+1

        np_image=np.array(input_image)
        np_mask=np.array(mask_image)
        
        np_image_big=np_image[y_bottom:y_top + 1, x_left:x_right + 1,:]
        np_mask_big=np_mask[y_bottom:y_top + 1, x_left:x_right + 1]

        mask_image = Image.fromarray(np_mask_big)
        init_image= Image.fromarray(np_image_big)

        init_image=init_image.resize((512,512),resample=Image.Resampling.LANCZOS)
        mask_image=mask_image.resize((512,512),resample=Image.Resampling.NEAREST)
        
        returned_image = None

        for ii in range(image_num):
            image = pipeline(prompt=prompt,image=init_image, mask_image=mask_image,strength=1.0).images[0]

            image=image.resize((new_H,new_W),resample=Image.Resampling.LANCZOS)
            np_origin=np.array(input_image)
            np_image=np.array(image)   
            np_origin[y_bottom:y_top + 1, x_left:x_right + 1,:]=np_image
            image= Image.fromarray(np_origin)

            image.save(save_path + '/num_' +str(ii)+ '.jpg')
            
            if ii == (image_num - 1):
                returned_image = image
        
        return returned_image, save_path + '/num_5.jpg'

    else:
    
        init_image=input_image.resize((512,512),resample=Image.Resampling.LANCZOS)
        mask_image=mask_image.resize((512,512),resample=Image.Resampling.NEAREST)
        returned_image = None
        
        for ii in range(image_num):
            image = pipeline(prompt=prompt,image=init_image, mask_image=mask_image,strength=1.0).images[0]
            image.save(save_path + '/num_' +str(ii)+ '.jpg')
            
            if ii == (image_num - 1):
                returned_image = image
        
        return returned_image, save_path + '/num_5.jpg'