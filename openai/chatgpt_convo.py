from openai import OpenAI

client = OpenAI()

model = "gpt-4o"
system = {"role": "developer", 
          "content": 
    "You are a world class mathematician and coder, you are helping to"
    "explain concepts to extremely bright PhD graduates from another "
    "discipline who understand a lot of basic concepts but do not have a "
    "firm grasp on calculus and linear algebra"}
messages = [
    {
        "role": "user",
        "content": [{"type": "text", "text": "Why is the ocean salty?"}],
    }
]

response = client.responses.create(
        model=model,
        input=[system, messages]
        )

print(response.output_text)
