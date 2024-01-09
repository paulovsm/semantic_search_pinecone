import json
import requests
import os
from django.http import JsonResponse
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.utilities.dalle_image_generator import DallEAPIWrapper
from langchain.schema import HumanMessage, SystemMessage
from .config import SYSTEM_PROMPT
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

# Define Django endpoint for a Post request to /chat
# Path: search/personal_stylist_view.py
@csrf_exempt
def recommendation(request):
    # Get the query string from the request JSON body
    data = json.loads(request.body)
    query_string = data.get("prompt")

    # Initialize the chat model
    chat = ChatOpenAI(
        temperature=1, 
        max_tokens=2048, 
#        model="gpt-4-1106-preview",
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" }
    )

    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT,
        ),
        HumanMessage(
            content=query_string
        ),
    ]

    # Generate the response
    chat_response = chat(messages)

    return JsonResponse(json.loads(chat_response.content), safe=False)

# Define Django endpoint for a Post request to /generateImage
# Path: search/personal_stylist_view.py
@csrf_exempt
def generateImage(request):
    # Get the query string from the request JSON body
    data = json.loads(request.body)
    query_string = data.get("prompt")
    engine = data.get("engine")
    image_url = ""
    image_b64 = ""

    if engine == "sdxl":
        # Initialize the image generator
        headers = {"Authorization": "Bearer " + os.getenv("EDEN_AI_API_KEY")}
        url = "https://api.edenai.run/v2/image/generation"
        payload = {
            "response_as_dict": True,
            "attributes_as_list": False,
            "show_original_response": False,
            "settings": "{ \"stabilityai\": \"stable-diffusion-xl-1024-v1-0\" }",
            "resolution": "1024x1024",
            "num_images": 1,
            "providers": "stabilityai",
            "text": query_string,
        }

        # Generate the image
        response = requests.post(url, json=payload, headers=headers)
        result = json.loads(response.text)
        image_b64 = result["stabilityai"]["items"][0]["image"]
    else:
        # Initialize the chat model
        client = OpenAI()

        response = client.images.generate(
            model="dall-e-3",
            prompt = query_string,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
    

    json_response = {
        "image_b64": image_b64,
        "image_url": image_url,
    }
    
    return JsonResponse(json_response, safe=False)