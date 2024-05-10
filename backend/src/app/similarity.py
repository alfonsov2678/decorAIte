import cohere
import torch
from pinecone.grpc import PineconeGRPC
from transformers import BitsAndBytesConfig
from transformers import pipeline
from PIL import Image
from gradio_client import Client

co = cohere.Client("6GIykOJ0sUGCKCMcTdM2Of1od5YMVFQYoIAC6CZs")
pc = PineconeGRPC(
    api_key='53403028-4cc9-495f-9b7c-90d977af0e9d',
    project_name="1fu0f0k"
)
index = pc.Index(host="https://decoraite-1fu0f0k.svc.aped-4627-b74a.pinecone.io")

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

model_id = "llava-hf/llava-1.5-7b-hf"
pipe = pipeline("image-to-text", model=model_id, model_kwargs={"quantization_config": quantization_config})

def find_product_similarity(image):
    prompt = "USER: <image>\nWhat is the largest item in the image? What is the shape, color and style (minimalist, modern, contemporary, etc.) of the largest item? Only return this 1 sentence description. \nASSISTANT:"

    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})
    caption = outputs[0]['generated_text'].split('ASSISTANT: ')[1]
    print(f'CAPTION: {caption}')

    # DENSE EMBEDDING
    response = co.embed(
        texts=[caption], model="embed-english-v3.0", input_type="classification"
    )
    
    dense  = response.embeddings[0]

    client = Client("https://agtm48-sparse-embedding.hf.space")
    
    # USE BM25 FOR SPARSE
    sparse = client.predict(caption, api_name='/predict')

    dense_final, sparse_final = hybrid_scale(dense, sparse, .85)

    results = index.query(
        vector=dense_final,
        sparse_vector=sparse_final,
        include_metadata=True,
        top_k=1)
    
    return results
    
def hybrid_scale(dense, sparse, alpha: float):
    # GOAL: scale sparse and dense vectors to create hybrid search vecs

    if alpha < 0 or alpha > 1:
        raise ValueError("Alpha must be between 0 and 1")
    hsparse = {
        'indices': sparse['indices'],
        'values':  [v * (1 - alpha) for v in sparse['values']]
    }
    hdense = [v * alpha for v in dense]
    return hdense, hsparse