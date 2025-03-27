import google.generativeai as genai
import dotenv
import os
import logging
from prompts import QUERY_CLASSIFICATION_PROMPT
import json

dotenv.load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def classify_query(query):
    try:
        logging.info(f"Classifying query: {query}")
        prompt = QUERY_CLASSIFICATION_PROMPT.format(
            query=query
        )
        response = model.generate_content(prompt)
        print(response)
        logging.info(f"Response: {response.text.strip()}")
        # Remove the ``` json ``` code block from the response
        response = response.text.strip().replace("```json", "").replace("```", "")
        response = json.loads(response)
        return response 
    except Exception as e:
        logging.error(f"Error classifying query: {e}")
        return "Unclear"
