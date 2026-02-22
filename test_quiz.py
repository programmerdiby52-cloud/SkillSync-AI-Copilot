import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
from pydantic import BaseModel, Field

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("NO API KEY")
    exit()

client = genai.Client(api_key=api_key)
MODEL_ID = 'gemini-1.5-flash'

class QuizQuestion(BaseModel):
    question: str = Field(description="The multiple choice question based on the text.")
    options: list[str] = Field(description="Exactly 4 distinct possible answers.", min_length=4, max_length=4)
    answer: str = Field(description="The exact string of the correct option from the options list.")

prompt = """
    Read the following text extracted from a university module PDF.
    Generate exactly 5 multiple choice questions to test the student's rigorous understanding of this specific material.
    
    TEXT:
    Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.
    Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured, object-oriented and functional programming.
"""

try:
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[QuizQuestion]
        )
    )
    print(response.text)
except Exception as e:
    print("ERROR:", e)
    import traceback
    traceback.print_exc()
