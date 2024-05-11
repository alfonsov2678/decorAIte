import os
from PIL import Image
import torch
from torchvision import transforms
import numpy as np
from torchmetrics.image.inception import InceptionScore





transform = transforms.Compose([
    transforms.Resize((299, 299)),  # Resize to 299x299
])


def resize_array(arr, target_height=299, target_width=299, channels=3):
    # Get the current dimensions of the array
    height, width, depth = arr.shape

    # Initialize the output array with zeros (padding) of the target size
    output_array = np.zeros((target_height, target_width, channels), dtype=arr.dtype)
    
    # Calculate padding sizes
    pad_height = (target_height - height) // 2
    pad_width = (target_width - width) // 2
    
    # Check if we need to crop or pad
    if height > target_height:
        # Calculate crop start index for height
        crop_height = (height - target_height) // 2
        arr = arr[crop_height:crop_height+target_height, :, :]
    elif height < target_height:
        # Pad height
        arr = np.pad(arr, ((pad_height, target_height - height - pad_height), (0, 0), (0, 0)), mode='constant')
    
    if width > target_width:
        # Calculate crop start index for width
        crop_width = (width - target_width) // 2
        arr = arr[:, crop_width:crop_width+target_width, :]
    elif width < target_width:
        # Pad width
        arr = np.pad(arr, ((0, 0), (pad_width, target_width - width - pad_width), (0, 0)), mode='constant')
    
    # Handle channel size differences
    if depth < channels:
        # If fewer channels, pad channels
        arr = np.pad(arr, ((0, 0), (0, 0), (0, channels - depth)), mode='constant')
    elif depth > channels:
        # If more channels, select the first three
        arr = arr[:, :, :channels]

    # Center the array in the output array if smaller
    start_height = (target_height - arr.shape[0]) // 2
    start_width = (target_width - arr.shape[1]) // 2
    output_array[start_height:start_height+arr.shape[0], start_width:start_width+arr.shape[1], :] = arr

    return output_array


def calculate_score(image_dir):
    inception = InceptionScore()

    for image_name in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_name)

        if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            try:
                image = Image.open(image_path).convert('RGB') 
                
                # print(np.array(image))
                
                tensor = torch.from_numpy(np.expand_dims(resize_array(np.array(image)).reshape(3,299,299),axis=0))
                
                # print(tensor.shape)
                
                inception.update(tensor)
                
                # print(tensor.shape)
                
                print(f"Converted {image_name} to a tensor successfully.")
            except Exception as e:
                print(f"Error processing {image_name}: {e}")

    mean, std  = inception.compute()
    print(f'Mean: {mean}, Standard Deviation: {std}')



if __name__ == "__main__":
    image_dir = 'controlnet_example_imgs'
    print('ControlNet score:')
    calculate_score(image_dir)

    image_dir = 'decoraite_example_imgs'
    print('decorAIte score:')
    calculate_score(image_dir)
