import numpy as np
import cv2
from gradio_client import Client, file
from PIL import Image

def generate_image(image_path, prompt):
  client = Client("MykolaL/StableDesign")
  result = client.predict(
      image=file(image_path),
      text=prompt,
      num_steps=50,
      guidance_scale=10,
      seed=88520596,
      strength=0.8,
      a_prompt="interior design, 4K, high resolution, photorealistic: " + prompt,
      n_prompt="window, door, low resolution, banner, logo, watermark, text, deformed, blurry, out of focus, surreal, ugly, beginner",
      img_size=768,
      api_name="/on_submit"
  )

  image = Image.open(result)
  image_np = np.array(image)
  image_np = image_np[:, :, ::-1]
  image_path = 'tmp/controlnet_output.png'
  cv2.imwrite(image_path, image_np)

  return image_path