from dotenv import load_dotenv
import anthropic

client= anthropic.Anthropic()
message= client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1000,
    messages=[
        {
            "role":"user",
            "content":" What should I search for to find latest development in generative ai?"
        }
    ],
)

for block in message.content:
    if block.type=="text":
        print(block.text)
        