import json
import requests
from dotenv import load_dotenv
from backend.gemini_parser import parse_intent

load_dotenv()

BACKEND_URL = "http://127.0.0.1:8000/acp"


def run_chat():
    print("ACP CLI — Gemini-powered (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            break

        if not user_input:
            continue

        try:
            parsed = parse_intent(user_input)
        except Exception as e:
            print(f"[Gemini error] {e}\n")
            continue

        if not parsed:
            print("Could not understand intent. Try: 'search for solar panels' or 'get product 5'\n")
            continue

        print(f"[ACP Message] {json.dumps(parsed, indent=2)}")

        try:
            response = requests.post(BACKEND_URL, json=parsed)
            data = response.json()
            results = data.get("data", [])
            print(f"\nAgent Response: {len(results)} result(s)")
            for item in results[:3]:
                print(f"  - {item.get('OfferName', 'N/A')} | {item.get('CompanyName', 'N/A')} | {item.get('Category', 'N/A')}")
            if len(results) > 3:
                print(f"  ... and {len(results) - 3} more")
        except Exception as e:
            print(f"[Backend error] {e}")

        print()


if __name__ == "__main__":
    run_chat()
