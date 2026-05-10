import os
import json
import logging
from openai import OpenAI
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logging.warning("OPENAI_API_KEY is not set. AI verification will fail.")
    return OpenAI(api_key=api_key) if api_key else None

def parse_with_ai(html_data: str, platform: str, query: str) -> List[Dict[str, Any]]:
    client = get_openai_client()
    if not client:
        return []

    # 30000 characters is a safe limit for typical responses and context bounds for GPT-4o
    truncated_data = html_data[:30000] if html_data else ""

    if not truncated_data:
        logging.warning(f"No data scraped for platform {platform}")
        return []

    system_prompt = """
    You are an AI Verification Engine for an Indonesian Marketplace Price Aggregator.
    Your task is to analyze the raw text/HTML extracted from a marketplace search page and return a strictly formatted JSON array containing the identified product items.

    CRUCIAL INSTRUCTIONS:
    1. Filter out "bait" prices (e.g., a seller listing an empty box, or an impossibly low price compared to the real product).
    2. Verify specs strictly: If the user searches for "DDR4 8GB 3200MHz", you MUST discard any results for DDR3, 4GB, or different speeds. The returned items must match the user's intent.
    3. Output ONLY valid JSON, as a JSON array of objects. Do not include markdown blocks like ```json or any other explanatory text.
    4. Each JSON object MUST have the exact following keys:
       - platform (string)
       - store_name (string)
       - product_name (string)
       - price (integer, parsed as a raw number without currency symbols)
       - link (string, try to extract or construct a valid URL if possible, otherwise use a placeholder)
       - condition (string, e.g., "New", "Used", "Unknown")
    """

    user_prompt = f"""
    Platform: {platform}
    User Search Query: "{query}"

    Raw Extracted Content:
    {truncated_data}

    Extract the most relevant and correctly matching products based on the user query. Output the JSON array.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0
        )

        output_text = response.choices[0].message.content.strip()

        if output_text.startswith("```json"):
            output_text = output_text[7:]
        if output_text.endswith("```"):
            output_text = output_text[:-3]

        parsed_json = json.loads(output_text.strip())

        if not isinstance(parsed_json, list):
            logging.error(f"AI Output is not a list: {parsed_json}")
            return []

        return parsed_json
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON from AI output: {e}. Raw Output: {output_text}")
        return []
    except Exception as e:
        logging.error(f"OpenAI API Error: {e}")
        return []
