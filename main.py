import os
import json
from dotenv import load_dotenv
import asyncio
import httpx
from openai import AsyncOpenAI
# 1. intialize OpenRouter via the OpenAI client wrapper
# OpenRouter requires the base_url to be explicitly pointed to their server.
load_dotenv()
cerebras_key = os.getenv("CEREBRAS_API_KEY")
if not cerebras_key:
    raise ValueError("CEREBRAS_API_KEY environment variable is not set.")
client = AsyncOpenAI(
    base_url="https://api.cerebras.ai/v1",
    api_key=cerebras_key,
)
async def fetch_with_retry(client: httpx.AsyncClient, url: str, params: dict, retries: int = 3) -> dict:
    for attempt in range(1, retries + 1):
        try:
            response = await client.get(url, params=params)
            return handle_response(response)
        except Exception as e:
            if attempt == retries:
                raise
            wait = 2 ** attempt
            print(f"Attempt {attempt} failed: {e} - retrying in {wait}s")
            await asyncio.sleep(wait)
async def fetch_crypto_trends() -> dict:
    """FETCHING DATA: Queries a public crypto API safely."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin,ethereum", "vs_currencies": "usd", "include_24hr_change": "true"}
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")
async def generate_crypto_report(trends: dict) -> str:
    """GENERATING CONTENT: Uses Cerebras to create a report based on the fetched data."""
    prompt = f"Generate a concise report on the current trends of Bitcoin and Ethereum based on the following data: {json.dumps(trends)}"
    response = await client.chat.completions.create(
        model="llama3.1-8b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content
def handle_response(response: httpx.Response) -> dict:
    """ERROR HANDLING: Validates and processes API responses."""
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            raise Exception("Invalid JSON response")
    else:
        raise Exception(f"API request failed with status code {response.status_code}")
async def main():
    """MAIN FUNCTION: Orchestrates the fetching and report generation."""
    try:
        trends = await fetch_crypto_trends()
        report = await generate_crypto_report(trends)
        print("Crypto Trends Report:")
        print(report)
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    asyncio.run(main())
    
    

