def enhance(input: str = "") -> tuple[str, str]:
    
    prompt: str = f"{input}, image, inpainting, missing parts, restoration, reconstruction, digital painting, realistic, seamless, high resolution"
    
    negative_prompt: str = "low resolution, blurry, distorted, unrealistic, inconsistent colors, pixelated"
    
    return prompt, negative_prompt
