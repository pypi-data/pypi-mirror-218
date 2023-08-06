def handsomizer(input: str = "") -> tuple[str, str]:
    
    prompt: str = f"{input}, male, selfie, handsome, attractive, charming, well-groomed, stylish, fashionable, good-looking, fit"
    
    negative_prompt: str = "unattractive, ugly, overweight, unshaven, scruffy, poorly-dressed, unkempt"
    
    return prompt, negative_prompt