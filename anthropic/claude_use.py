import anthropic

client = anthropic.Anthropic()

model = "claude-3-5-haiku-latest"
max_tokens = 1000
temperature = 1
system = (
    "You are a world class mathematician and coder, you are helping to"
    "explain concepts to extremely bright PhD graduates from another"
    "discipline who understand a lot of basic concepts but do not have a "
    "firm grasp on calculus and linear algebra"
)
messages = [
    {
        "role": "user",
        "content": [{"type": "text", "text": "Why is the ocean salty?"}],
    }
]


message = client.messages.create(
    model=model,
    max_tokens=max_tokens,
    temperature=temperature,
    system=system,
    messages=messages,
)
print(message.content)
