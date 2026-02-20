from pathlib import Path
from backend.agents.vendor_agent import VendorAgent
from backend.protocol import create_response

class Orchestrator:

    def __init__(self):
        file_path = Path(__file__).parent / "data" / "DewaStore List.xlsx"
        self.vendor = VendorAgent(
            agent_id="vendor_1",
            file_path=str(file_path)
        )

    def route(self, message: dict):

        intent = message["intent"]
        agent_id = message["agent_id"]
        payload = message["payload"]

        if agent_id == "vendor_1":
            result = self.vendor.handle(intent, payload)
            return create_response("success", result)

        return create_response("error", "Unknown agent")