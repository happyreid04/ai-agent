import asyncio
import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI
from main import fetch_crypto_trends
from datetime import datetime
import subprocess


load_dotenv()
cerebras_key = os.getenv("CEREBRAS_API_KEY")
if not cerebras_key:
    raise ValueError("CEREBRAS_API_KEY environment variable is not set.")
client = AsyncOpenAI(
    base_url="https://api.cerebras.ai/v1",
    api_key=cerebras_key,
)
def analyze(data: dict) -> dict:
    """Rule-based layer - extracts signals from raw data.
    No LLM involved. Fast and free."""
    btc_change = data["bitcoin"]["usd_24h_change"]
    eth_change = data["ethereum"]["usd_24h_change"]
    payload = json.dumps({
        "btc_change": btc_change,
        "eth_change": eth_change,
    })
    result = subprocess.run(
        ["./signals.exe"],
        input=payload,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise Exception(f"Signal analysis failed: {result.stderr}")
    return json.loads(result.stdout)
async def classify_mood(signals: dict) -> str:
    """LLM layer - reasons about the signals and returns a mood.
    only called after rule-based analysis."""
    prompt = f"""
    You are a crypto market analyst.
    Given these 24h market signals:
    - Bitcoin change: {signals['btc_change']:.2f}%
    - Ethereum change: {signals['eth_change']:.2f}%
    - Average change: {signals['avg_change']:.2f}%
    - Momentum score: {signals['momentum']:.2f}
    f"Both coins agree on direction: {signals['agreement']}"
    Classify the current market mood as exactly one word:
    bullish, bearish, or neutral.
    Respond with that one word only. No explanation."""
    response = await client.chat.completions.create(
        model="llama3.1-8b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
    )
    return response.choices[0].message.content.strip().lower()
def decide(mood: str, signals: dict):
    """Acts on the mood. This is where your agents personality lives.
    Right now it prints - later it can trigger anything."""
    actions = {
        "bullish": "Market is bulish - monitor for entry signals",
        "bearish": "Market is bearish - hold or reduce exposure",
        "neutral": "Market is neutral - wait for clearer signal",
    }
    print(f"\n Market Mood: {mood.upper()}")
    print(f" BTC: {signals['btc_change']:.2f}% | ETH: {signals['eth_change']:.2f}%")
    print(f" Action: {actions.get(mood, 'unknown mood retry')}")
async def run_brain(data: dict):
    signals = analyze(data)
    mood = await classify_mood(signals)
    decide(mood, signals)
async def main():
    print("Crypto Signal agent started...")
    print("Checking market every 60 min\n")
    cycle = 1
    while True:
        print(f"--- Cycle {cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        try:
            data = await fetch_crypto_trends()
            await run_brain(data)
        except Exception as e:
            print(f"Error in cycle {cycle}: {e}")
        cycle += 1
        print("\nNext check in 60 minutes...\n")
        await asyncio.sleep(3600)  # wait for 60 minutes before next check

if __name__ == "__main__":
    asyncio.run(main())

    
