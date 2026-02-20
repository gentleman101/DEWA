import os
import json
from google import genai
from google.genai import types

SYSTEM_PROMPT = """
You are an intent parser for an ACP (Agent Communication Protocol) system.
A user will type a natural language message. You must return a JSON object with exactly these fields:

{
  "intent": "<intent_name>",
  "agent_id": "vendor_1",
  "payload": { ... }
}

Available intents:
1. search_product — search offers/products by keyword
   payload: { "keyword": "<word>" }

2. get_product — retrieve a specific product by its numeric ID
   payload: { "product_id": "<number>" }

Rules:
- Always return raw JSON only. No markdown, no explanation, no code fences.
- If the user's message does not match any intent, return: { "error": "unknown intent" }
- For search_product, extract the most relevant keyword from the user's message.
"""


def parse_intent(user_input: str) -> dict | None:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=os.environ["GEMINI_MODEL"],
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0,
        )
    )
    raw = response.text.strip()
    parsed = json.loads(raw)
    if "error" in parsed:
        return None
    return parsed
