# Prompt Pilot

*DISCLAIMER: This is a work in progress, and I'm sharing it as a temporary solution with some functions that you can experiment with.*

Prompt Pilot is a library designed for prompt engineering in AI models. It introduces the concept of "prompt functions" to streamline the prompt creation process. With just one function, developers can create complex prompts effortlessly.

Here's an example implementation for creating a digital marketing chatbot:

```
# import the required functions from prompt_pilot
from prompt_pilot.assistants import digital_marketing_analyst 
from prompt_pilot.api_ai import stablelm

# configure your apikey
api_key = config("REPLICATE_API_TOKEN") 
# use promptpilot to generate prompt
prompt = digital_marketing_analyst() 
# use promptpilot's api call functions to pass prompt and apikey. Here, we are using the StableLM model
output = stablelm(prompt, api_key)

print(output)
```

By automating both prompt engineering and API calls to AI models, Prompt Pilot significantly reduces the code required to build a chatbot. With just 5-6 lines of code, you can have a fully functional chatbot up and running in very little time.

Here's what you can build with prompt-pilot:

- Chatbots and other NLP tasks : Personalized chatbots for business usecase, personal usecase, and academic usecase. API calls to OpenAI and LLMs on Replicate
- Image models : Varying styles for image generators. API calls to image models on Replicate
- Data science : Automating data-science by incorporating LLMs (OpenAI) into the process to perform analysis
