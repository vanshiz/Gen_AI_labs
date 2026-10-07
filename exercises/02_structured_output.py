"""Exercise 2: ticket classifier with validated JSON.
Setup: pip install anthropic pydantic python-dotenv
TODO: run on 20 tickets, compute accuracy against labels you write by hand.
"""
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal
import anthropic

load_dotenv()
client = anthropic.Anthropic()


class Triage(BaseModel):
    category: Literal["billing", "bug", "feature_request", "other"]
    urgency: Literal["low", "medium", "high"]
    summary: str


PROMPT = """Classify the support ticket inside <ticket> tags.
Reply with ONLY a JSON object: {{"category": ..., "urgency": ..., "summary": ...}}
category is one of billing|bug|feature_request|other; urgency is low|medium|high.

<ticket>{ticket}</ticket>"""


def triage(ticket: str) -> Triage:
    msg = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=300,
        temperature=0,
        messages=[{"role": "user", "content": PROMPT.format(ticket=ticket)}],
    )
    return Triage.model_validate(json.loads(msg.content[0].text))


if __name__ == "__main__":
    print(triage("I was charged twice this month and need a refund ASAP!"))
