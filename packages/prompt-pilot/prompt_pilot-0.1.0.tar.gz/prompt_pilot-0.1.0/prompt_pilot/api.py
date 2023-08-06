import replicate

def replicate_stablelm(prompt: str = "", api_key: str = ""):
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

    # for item in output:
    #     print(item)
