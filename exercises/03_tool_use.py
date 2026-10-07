"""Exercise 3: the tool-use loop, written by hand.
Setup: pip install anthropic python-dotenv
TODO: add a search_files tool (validate paths!), then an iteration cap of 10.
"""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

tools = [
    {
        "name": "calculator",
        "description": "Evaluate a basic arithmetic expression like '12 * (3 + 4)'.",
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
    },
    {
        "name": "get_weather",
        "description": "Get current weather for a city (fake data for the exercise).",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
]


def run_tool(name: str, args: dict) -> str:
    if name == "calculator":
        expr = args["expression"]
        if not set(expr) <= set("0123456789+-*/(). "):  # never eval untrusted input blindly
            raise ValueError("invalid characters")
        return str(eval(expr, {"__builtins__": {}}))
    if name == "get_weather":
        return f"{args['city']}: 31C, sunny"
    raise ValueError(f"unknown tool {name}")


messages = [{"role": "user", "content": "What's the weather in Delhi, and what is 31 * 9 / 5 + 32?"}]
for _ in range(10):  # iteration cap
    resp = client.messages.create(
        model="claude-sonnet-5-5", max_tokens=1024, tools=tools, messages=messages
    )
    messages.append({"role": "assistant", "content": resp.content})
    if resp.stop_reason != "tool_use":
        print(next(b.text for b in resp.content if b.type == "text"))
        break
    results = []
    for block in resp.content:
        if block.type == "tool_use":
            try:
                out, is_err = run_tool(block.name, block.input), False
            except Exception as e:  # let the model see and recover from errors
                out, is_err = str(e), True
            results.append(
                {"type": "tool_result", "tool_use_id": block.id, "content": out, "is_error": is_err}
            )
    messages.append({"role": "user", "content": results})
