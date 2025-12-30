import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

MODEL = "meta-llama/Llama-3.1-8B-Instruct"
API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}



class InvalidLLMResponse(Exception):
    pass


def validate_project_profile(data: dict):
    if not isinstance(data, dict):
        raise InvalidLLMResponse("LLM output is not a JSON object")

    if "name" not in data or not isinstance(data["name"], str):
        raise InvalidLLMResponse("Field 'name' must be a string")

    if "budget_inr_per_month" not in data or not isinstance(
        data["budget_inr_per_month"], (int, float)
    ):
        raise InvalidLLMResponse("Field 'budget_inr_per_month' must be a number")

    if data["budget_inr_per_month"] < 0:
        raise InvalidLLMResponse("budget_inr_per_month cannot be negative")

    if "tech_stack" not in data or not isinstance(data["tech_stack"], dict):
        raise InvalidLLMResponse("Field 'tech_stack' must be an object")


    if "non_functional_requirements" not in data or data["non_functional_requirements"] is None:

        data["non_functional_requirements"] = []

    if not isinstance(data["non_functional_requirements"], list):
        raise InvalidLLMResponse(
            "Field 'non_functional_requirements' must be a list"
        )


# ------------------- LLM Call -------------------

def extract_project_profile(description_text: str) -> dict:
    prompt = f"""
You are a cloud solution architect.

Extract a structured project profile from the text below and output ONLY valid JSON.

Guidelines:
- Infer a reasonable project name based on the project description.
- Extract the monthly budget in INR if mentioned.
- Summarize the project purpose briefly in the description field.
- Extract the technology stack where explicitly mentioned.
- If a technology or detail is not mentioned, use null.
- Extract non-functional requirements only if they are explicitly stated.

Text:
{description_text}

Return JSON with the following top-level fields:
- name
- budget_inr_per_month
- description
- tech_stack
- non_functional_requirements
"""


    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that outputs ONLY valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1,
        "max_tokens": 512
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()

    output_text = response.json()["choices"][0]["message"]["content"].strip()

    if output_text.startswith("```"):
        output_text = output_text.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
    if output_text.lower().startswith("json"):
        output_text = output_text[4:].strip()

    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError:
        raise InvalidLLMResponse(
            f"Invalid JSON from LLM\n\nRaw Output:\n{output_text}"
        )

    validate_project_profile(parsed)
    return parsed
