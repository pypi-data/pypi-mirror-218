# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 14:19:34 2023

@author: גלעד
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 21:07:47 2023

@author: Academy4summer
"""
import requests
import openai
from urllib3.exceptions import InsecureRequestWarning
 
# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class AcademyAI:
    def __init__(self, api_key):
        self.api_key = api_key

    def ask_AI(self, question):
        
        openai.api_key = self.api_key
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="You: "+ question,
            temperature=0.5,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=["You:"],
            verify = False
            )
        
        text = response["choices"][0]["text"]
        return text
    def paint_AI(self, prompt):
        # Set up API endpoint and headers for Dall-E 2
        endpoint = "https://api.openai.com/v1/images/generations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

        # Define the request payload with the input prompt
        payload = {
            "model": "image-alpha-001",
            "prompt": prompt,
            "num_images":1,
            "size":"1024x1024",
            "response_format":"url"
        }

        # Make the API request to OpenAI and get the response
        response = requests.post(endpoint, headers=headers, json=payload ,verify = False)

        # Extract the image URL from the response and return it
        response_data = response.json()
        if "data" in response_data:
            image_url = response_data["data"][0]["url"]
        else:
            image_url = "Sorry, the response from the API was not in the expected format."
        return image_url
    

