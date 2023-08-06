# Prompt Pilot

*DISCLAIMER: It's currently in development and I am uploading this primarily as a placeholder with some functions that you guys can play around with.*

Prompt Pilot is a prompt engineering library for AI models that introduces the concept of "prompt functions" to augement the process of prompt engineering. It allows developers to create complex prompts with just one function.

Example implementation for creating a digital marketing chatbot:

```
# import the required functions from prompt_pilot
from prompt_pilot.assistants import developer, digital_marketing_analyst 
from prompt_pilot.api import replicate_stablelm

# configure your apikey
api_key = config("REPLICATE_API_TOKEN") 
# use promptpilot to generate prompt
prompt = digital_marketing_analyst() 
# use promptpilot's api call functions to pass prompt and apikey. Here, we are using the StableLM model
output = replicate_stablelm(prompt, api_key)

print(output)
```

This automates both prompt engineering and API calls that we make to AI models and cuts down the whole process to just 5-6 lines of code.
