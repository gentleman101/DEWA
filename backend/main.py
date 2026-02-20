from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from backend.protocol import create_message
from backend.orchestrator import Orchestrator
from backend.gemini_parser import parse_intent

load_dotenv()

app = FastAPI(title="ACP Demo System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

orch = Orchestrator()

frontend_path = Path(__file__).parent.parent / "frontend"
app.mount("/ui", StaticFiles(directory=str(frontend_path), html=True), name="frontend")


class RequestModel(BaseModel):
    intent: str
    agent_id: str
    payload: dict = {}


class ChatRequest(BaseModel):
    query: str


@app.post("/acp")
def acp_endpoint(req: RequestModel):
    message = create_message(
        intent=req.intent,
        agent_id=req.agent_id,
        payload=req.payload
    )
    response = orch.route(message)
    return response


@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    parsed = parse_intent(req.query)
    if not parsed:
        return {"error": "Could not understand intent"}

    message = create_message(
        intent=parsed["intent"],
        agent_id=parsed["agent_id"],
        payload=parsed["payload"]
    )

    acp_response = orch.route(message)
    top3 = acp_response.get("data", [])[:3]

    return {
        "top3": top3,
        "acp_request": message,
        "acp_response": acp_response
    }
