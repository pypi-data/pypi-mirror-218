import openai
import replicate
from PIL import Image

# This script has a good set of handpicked models for both NLP (GPT-3.5,4) and CV (StableDiffusion) tasks. HuggingFace API to be added later if needed. 

# Language models
# ----------------------------------------------------------------

def gpt3(api_key:str = "", prompt:str = ""):

    openai.api_key = api_key
    
    completion = openai.ChatCompletion.create(
    
    model="gpt-3.5-turbo-0613",
    messages= [{"role": "system", "content": prompt}])

    response = completion.choices[0].message
    return response

def gpt4(api_key:str = "", prompt:str = ""):

    openai.api_key = api_key
    
    completion = openai.ChatCompletion.create(
    
    model="gpt-4-0613",
    messages= [{"role": "system", "content": prompt}])

    response = completion.choices[0].message
    return response

def stablelm_7b(api_key: str = "", prompt: str = ""):
    
    client = replicate.Client(api_token=api_key)

    output = client.run(
        "stability-ai/stablelm-tuned-alpha-7b:c49dae362cbaecd2ceabb5bd34fdb68413c4ff775111fea065d259d577757beb",
        input={
            "prompt": prompt,
            "max_tokens": 500,
            "top_p": 1,
            "temperature": 0.75,
            "repetition_penalty": 1.2
        }
    )

    response = ''.join(output)
    return response

def vicuna_13b(api_key: str = "", prompt: str = ""):
    
    client = replicate.Client(api_token=api_key)

    output = client.run(
        "replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b",
        input={
            "prompt": prompt,
            "max_tokens": 50,
            "top_p": 1,
            "temperature": 0.75,
            "repetition_penalty":1.2
            }
    )

    response = ''.join(output)
    return response

def flan_t5_xl(api_key: str = "", prompt: str = ""):
    
    client = replicate.Client(api_token=api_key)

    output = client.run(
        "replicate/flan-t5-xl:7a216605843d87f5426a10d2cc6940485a232336ed04d655ef86b91e020e9210",
        input={
            "prompt": prompt,
            "max_tokens": 50,
            "top_p": 1,
            "temperature": 0.75,
            "repetition_penalty":1.2
            }
    )

    response = ''.join(output)
    return response

# Image models
# ----------------------------------------------------------------

def stable_diffusion(api_key: str = "", prompt: str = "", negative_prompt: str = ""):

    client = replicate.Client(api_token=api_key)

    output = client.run(
        "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
        input={
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "image_dimensions": "512x512",
            "num_outputs": 1,
            "num_inference_steps": 50,
            "guidance_scale": 7.5,
            "scheduler": "DPMSolverMultistep",
            # "seed": ,
            }
    )

    print(output)

# def stable_diffusion_img2img(api_key: str = "", prompt: str = "", negative_prompt: str = "", image:str = ""):

#     client = replicate.Client(api_token=api_key)

#     output = client.run(
#         "stability-ai/stable-diffusion-img2img:15a3689ee13b0d2616e98820eca31d4c3abcd36672df6afce5cb6feb1d66087d",
#         input={
#             "prompt": prompt,
#             "negative_prompt": negative_prompt,
#             "image": image,
#             "prompt_strength": 0.8,
#             "num_outputs": 1,
#             "num_inference_steps": 25,
#             "guidance_scale": 7.5,
#             "scheduler": "DPMSolverMultistep",
#             # "seed": ,
#             }
#     )

#     print(output)

# def stable_diffusion_inpainting(api_key: str = "", prompt: str = "", negative_prompt: str = "", image_path: str = "", mask_path: str = ""):
#     # Convert file paths to image files

#     client = replicate.Client(api_token=api_key)
#     output = client.run(
#         "stability-ai/stable-diffusion-inpainting:c28b92a7ecd66eee4aefcd8a94eb9e7f6c3805d5f06038165407fb5cb355ba67",
#         input={
#             "prompt": prompt,
#             "negative_prompt": negative_prompt,
#             "image": Image.open(image_path),
#             "mask": Image.open(mask_path),
#             "num_outputs": 1,
#             "num_inference_steps": 25,
#             "guidance_scale": 7.5,
#             # "seed": ,
#         }
#     )
#     print(output)

def gfpgan(api_key: str = "", image_url: str = ""):

    client = replicate.Client(api_token=api_key)

    output = client.run(
        "tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3",
        input={"img": open(image_url, "rb")}
    )

    print(output)