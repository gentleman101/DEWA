# DEWA Assistant — ACP Demo

A demo of Agent Communication Protocol (ACP) with a Gemini-powered natural language interface and a browser-based search UI.

---

## Project Structure

```
ACP_Demo/
├── backend/
│   ├── agents/
│   │   └── vendor_agent.py       # Searches the Excel product data
│   ├── data/
│   │   └── DewaStore List.xlsx   # Product/offer dataset
│   ├── gemini_parser.py          # Shared Gemini intent parser
│   ├── orchestrator.py           # Routes ACP messages to agents
│   ├── protocol.py               # ACP message/response builders
│   └── main.py                   # FastAPI server (ACP + Chat endpoints)
├── frontend/
│   └── index.html                # Browser UI (DEWA Assistant)
├── user_layer/
│   └── cli_chat.py               # CLI interface (natural language → ACP)
├── .env                          # API keys (not committed)
├── requirements.txt
└── README.md
```

---

## Prerequisites

- Python 3.11+
- A Gemini API key — get one free at [aistudio.google.com](https://aistudio.google.com/apikey)

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your API key

Open `.env` in the project root and paste your Gemini API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

> To switch models, change `GEMINI_MODEL` — e.g. `gemini-2.0-flash-lite`, `gemini-1.5-pro`.

---

## Running the App

### Start the backend server

Run from the project root (`ACP_Demo/`):

```bash
python -m uvicorn backend.main:app --reload
```

The server starts at `http://127.0.0.1:8000`

---

## Using the App

### Option A — Browser UI (DEWA Assistant)

Open in your browser:

```
http://127.0.0.1:8000/ui/index.html
```

- Type a natural language query and press **Search** or Enter
- Top 3 matching offers appear as cards
- Click **Protocols** (top-right) to inspect the full ACP JSON communication

Example queries:
```
find me solar panel deals
show insurance offers
smart home products
discount on relocation
```

---

### Option B — CLI Chat

Open a second terminal and run:

```bash
python -m user_layer.cli_chat
```

Example session:
```
You: find me solar panel deals
[ACP Message] { "intent": "search_product", "agent_id": "vendor_1", "payload": { "keyword": "solar" } }

Agent Response: 4 result(s)
  - Vista Eco Solar Solutions LLC | Vista Eco | Service
  ...

You: get product 5
You: exit
```

---

### Option C — Swagger (raw ACP API)

Open in your browser:

```
http://127.0.0.1:8000/docs
```

**Search products:**
```json
POST /acp
{
  "intent": "search_product",
  "agent_id": "vendor_1",
  "payload": { "keyword": "solar" }
}
```

**Get a product by ID (0–1256):**
```json
POST /acp
{
  "intent": "get_product",
  "agent_id": "vendor_1",
  "payload": { "product_id": "5" }
}
```

---

## How It Works

```
Browser / CLI
     |
     | natural language query
     v
Gemini (gemini-2.0-flash)
     |
     | structured ACP message
     | { protocol, message_id, timestamp, intent, agent_id, payload }
     v
Orchestrator  —routes by agent_id—>  VendorAgent
                                          |
                                          | searches Excel data
                                          v
                                      ACP Response
                                { protocol, status, data[] }
```

### ACP Message Format

```json
{
  "protocol": "ACP/1.0",
  "message_id": "uuid-here",
  "timestamp": "2026-02-20T10:00:00",
  "intent": "search_product",
  "agent_id": "vendor_1",
  "payload": { "keyword": "solar" }
}
```

### ACP Response Format

```json
{
  "protocol": "ACP/1.0",
  "status": "success",
  "data": [ { "OfferName": "...", "CompanyName": "...", ... } ]
}
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/acp` | Raw ACP endpoint — accepts structured intent/payload |
| `POST` | `/chat` | Web UI endpoint — accepts natural language, calls Gemini internally |
| `GET`  | `/ui/index.html` | Serves the browser UI |
| `GET`  | `/docs` | Swagger UI |
