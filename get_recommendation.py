import google.generativeai as genai
import dotenv
import os
import logging
from prompts import RECOMMENDATION_PROMPT

dotenv.load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def get_recommendation(query, category):
    try:
        logging.info(f"Getting recommendation for query: {query}")
        prompt = RECOMMENDATION_PROMPT.format(
            query=query, category=category
        )
        response = model.generate_content(prompt)
        logging.info(f"Response: {response.text.strip()}")
        return response.text.strip()
    except Exception as e:
        logging.error(f"Error getting recommendation: {e}")
        return "Unable to provide recommendation"