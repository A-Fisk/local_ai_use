from openai import OpenAI
import os
import textwrap
from typing import List, Dict, Any, Optional, Union
from rich.console import Console
from rich.markdown import Markdown

# create console object for printing pretty markdown
console = Console()

# define model parameters
model = "gpt-4o"
max_tokens = 10000
temperature = 1
system = (
    "You are a world class mathematician and coder, you are helping to"
    "explain concepts to extremely bright PhD graduates from another"
    "discipline who understand a lot of basic concepts but do not have a "
    "firm grasp on calculus and linear algebra. Please format your output in"
    "markdown format, but the result will be output in a terminal so avoid "
    "using latex equations. "
    "Please use the correct english spelling for all outputs,"
    " such as colour and maths"
)
reasoning_enabled = True


# create function to create chat interface
def create_chat_interface(
    model: str,
    max_tokens: int,
    temperature: float,
    system: str,
    reasoning_enabled: bool = False,
):
    # Initialize the OpenAI client
    client = OpenAI()

    # Store conversation history
    messages = []
    reasoning_outputs = []
    
    # Add system message to start
    messages.append({
        "role": "system",
        "content": system
    })

    print("\n=== GPT Chat Interface ===")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:

        # Get user input
        print("\n---- Press CTRL+D to send. You: ")
        lines = []

        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            # This happens when the user presses Ctrl+D
            pass

        user_input = "\n".join(lines)

        # Check for exit command
        if user_input.lower() in ["exit", "quit"]:
            print("\nEnding conversation. Goodbye!")
            break

        # Add user message to history
        messages.append(
            {"role": "user", "content": user_input}
        )

        print("\nGPT is thinking...")

        try:
            if reasoning_enabled:
                # First get reasoning with separate call
                reasoning_prompt = messages.copy()
                reasoning_prompt.append({
                    "role": "system",
                    "content": "Think step-by-step about how to respond to the user's request. Show your reasoning process."
                })
                
                reasoning_response = client.chat.completions.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=reasoning_prompt,
                )
                
                reasoning_text = reasoning_response.choices[0].message.content
                reasoning_outputs.append(reasoning_text)
                
                # Now get actual response
                response = client.chat.completions.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=messages,
                )
            else:
                # Just get normal response
                response = client.chat.completions.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=messages,
                )

            # Extract the response text
            assistant_message = response.choices[0].message.content

            # Add assistant's response to history
            messages.append(
                {
                    "role": "assistant",
                    "content": assistant_message,
                }
            )

            # Display the response with nice formatting
            print("\n--------- GPT:")

            # display reasoning if enabled
            if reasoning_enabled:
                print("\n----- thinking:")
                console.print(Markdown(reasoning_text))
                print("\n----- responding:")

            # display response with markdown format
            console.print(Markdown(assistant_message))

        except Exception as e:
            print(f"\nAn error occurred: {e}")

    # return the output so can play with after
    return messages, reasoning_outputs if reasoning_enabled else []


if __name__ == "__main__":
    message_log, reasoning_log = create_chat_interface(
        model, max_tokens, temperature, system, reasoning_enabled
    )