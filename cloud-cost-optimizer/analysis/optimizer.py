import os
import json
import requests
import re
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
MODEL = "meta-llama/Llama-3.1-8B-Instruct"
API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

def extract_json_object(text: str) -> dict:
    """Helper to extract JSON object from LLM response."""
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if not match:
            return None
        json_str = match.group(0)

        json_str = re.sub(r',\s*\}', '}', json_str)
        json_str = re.sub(r',\s*\]', ']', json_str)
        return json.loads(json_str)
    except Exception as e:
        print(f"Extraction Error: {e}")
        return None

def generate_optimization_report(profile: dict, billing: list ,analyzer :dict) -> dict:
    """Uses LLM to analyze billing and profile to generate recommendations."""
    
    prompt = f"""
As a Cloud FinOps Architect, analyze the following project data and generate a Cost Optimization Report.

PROJECT CONTEXT:
{json.dumps(profile, indent=2)}

ACTUAL BILLING DATA:
{json.dumps(billing, indent=2)}

STRICT RULES:
1. Provide exactly 6–10 recommendations.
2. Include Multi-cloud alternatives (AWS, Azure, GCP, DigitalOcean) and Open-Source options.
5. Ensure 'potential_savings' are realistic based on the 'current_cost'.
Use the following PRE-COMPUTED COST ANALYSIS (do NOT recalculate numbers):

COST ANALYSIS:
{json.dumps(analyzer, indent=2)}

Output ONLY a JSON object in this format:
{{
  "project_name": "string",
  "analysis": {{
    "total_monthly_cost": number,
    "budget": number,
    "budget_variance": number,
    "service_costs": {{ "ServiceName": cost }},
    "high_cost_services": {{ "ServiceName": cost }},
    "is_over_budget": boolean
  }},
  "recommendations": [
    {{
      "title": "string",
      "service": "string",
      "current_cost": number,
      "potential_savings": number,
      "recommendation_type": "open_source|free_tier|alternative_provider|optimization|right_sizing",
      "description": "string",
      "implementation_effort": "low|medium|high",
      "risk_level": "low|medium|high",
      "steps": ["step 1", "step 2"],
      "cloud_providers": ["Provider names"]
    }}
  ],
  "summary": {{
    "total_potential_savings": number,
    "savings_percentage": number,
    "recommendations_count": number,
    "high_impact_recommendations": number
  }}
}}
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional cloud cost analyst. Output ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 3000
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    response.raise_for_status()
    
    output_text = response.json()["choices"][0]["message"]["content"]
    return extract_json_object(output_text)

