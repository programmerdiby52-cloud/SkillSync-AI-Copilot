import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import json

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

class WeekPlan(BaseModel):
    week: str = Field(description="Week number and topic, e.g., 'Week 1: Python Basics'")
    goal: str = Field(description="The primary objective for this week.")
    resources: list[str] = Field(description="List of exactly 3 markdown links to real YouTube videos, GeeksforGeeks, or Coursera.")

try:
    print("Sending request...")
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents="Generate a 1-week roadmap for a QA tester.",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[WeekPlan]
        )
    )
    print("Response text:", response.text)
    print("Parsed JSON:", json.loads(response.text))
except Exception as e:
    print("ERROR:", e)
