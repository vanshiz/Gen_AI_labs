"""Exercise 1: multi-turn streaming chatbot.
Setup: pip install anthropic python-dotenv ; put ANTHROPIC_API_KEY in .env
Run:   python exercises/01_first_call.py
TODO: add a system prompt, token usage printing, and retry on errors.
"""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
history = []  # the API is stateless: you resend the whole conversation

while True:
    user = input("you> ").strip()
    if user in {"exit", "quit"}:
        break
    history.append({"role": "user", "content": user})
    with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        system="You are a concise tutor for generative AI.",
        messages=history,
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
        final = stream.get_final_message()
    print(f"\n[tokens in={final.usage.input_tokens} out={final.usage.output_tokens}]")
    history.append({"role": "assistant", "content": final.content})
