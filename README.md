# ai-agent
# Crypto Signal Agent

An AI-powered crypto market signal generator built with Python, Nim, and Qwen LLM. Fetches live Bitcoin and Ethereum data, processes market signals at native speed via Nim, and classifies market mood every hour using a large language model.

---

## Architecture

```
CoinGecko API
      ↓
main.py          — async data fetching, retry logic, error handling
      ↓
signals.exe      — Nim binary, fast numeric processing
      ↓
orchestrator.py  — agent brain, LLM classification, decision layer
      ↓
Signal Output    — BULLISH / BEARISH / NEUTRAL every hour
```

---

## Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Data | CoinGecko API | Live BTC/ETH price data |
| HTTP | httpx | Async HTTP client |
| Processing | Nim | Fast numeric signal calculation |
| LLM | Cerebras + Qwen | Market mood classification |
| Orchestration | Python asyncio | Agent loop and decision logic |

---

## Features

- Async data fetching with retry and exponential backoff
- Nim-powered numeric processing — momentum, volatility, direction agreement
- LLM mood classification — bullish, bearish, or neutral
- Continuous loop — checks market every hour
- Error recovery — one failed cycle doesn't stop the agent
- Clean two-file architecture — data layer and brain layer separated

---

## Project Structure

```
AI-agent/
├── main.py          # Data pipeline — fetches crypto prices from CoinGecko
├── orchestrator.py  # Agent brain — signals, LLM classification, decisions
├── signals.nim      # Nim source — numeric processing logic
├── signals.exe      # Compiled Nim binary
├── .env             # API keys — never committed to git
├── .gitignore       # Excludes .env and other sensitive files
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/happyreid04/AI-agent.git
cd AI-agent
```

### 2. Install Python dependencies

```bash
pip install httpx openai python-dotenv
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```
CEREBRAS_API_KEY=csk-...
```

Get your free Cerebras API key at [cloud.cerebras.ai](https://cloud.cerebras.ai)

### 4. Compile the Nim binary

Make sure Nim is installed, then:

```bash
nim compile --opt:speed -o:signals signals.nim
```

### 5. Run the agent

```bash
python orchestrator.py
```

---

## Example Output

```
Crypto Signal Agent started...
Checking market every 60 minutes

--- Cycle 1 | 2026-05-19 11:38:14 ---
 Market Mood: BEARISH
 BTC: 0.33% | ETH: 1.02%
 Action: Market is bearish — hold or reduce exposure

Next check in 60 minutes...
```

---

## How It Works

### 1. Data Layer — `main.py`
Fetches 24h price change data for Bitcoin and Ethereum from the CoinGecko public API using async HTTP. Includes retry logic with exponential backoff to handle rate limits and transient failures.

### 2. Signal Processing — `signals.nim`
Receives raw price data via stdin as JSON, calculates numeric signals including average change, momentum score, and direction agreement between BTC and ETH. Returns enriched signals as JSON via stdout.

### 3. Agent Brain — `orchestrator.py`
Passes signals to Qwen LLM via Cerebras API with a tight classification prompt. The LLM returns a single word — bullish, bearish, or neutral. The decision layer maps that mood to a recommended action and prints the signal.

---

## Roadmap

- [ ] Push signals to a Telegram or Discord alert
- [ ] Add more tokens — SOL, BNB, AVAX
- [ ] Deploy to a cloud server for 24/7 operation
- [ ] Add signal history logging to a file or database
- [ ] Nim volatility scoring across multiple timeframes

---

## AUTHOR
Happyreid04

---

## License

MIT
