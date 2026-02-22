from google import genai
from google.genai import types

import inspect

try:
    print(inspect.signature(types.Part.from_text))
except Exception as e:
    print("Error:", e)

try:
    part1 = types.Part.from_text("Hello")
    print("Positional works")
except Exception as e:
    print("Positional error:", e)

try:
    part2 = types.Part.from_text(text="Hello")
    print("Keyword works")
except Exception as e:
    print("Keyword error:", e)
