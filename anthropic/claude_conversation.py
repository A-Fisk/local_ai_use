import anthropic
import os
import textwrap
from typing import List, Dict, Any, Optional, Union
from rich.console import Console
from rich.markdown import Markdown

# create console object for printing pretty markdown
console = Console()

# define model parameters
model = "claude-3-5-haiku-latest"
max_tokens = 1000
temperature = 1
system = (
    "You are a world class mathematician and coder, you are helping to"
    "explain concepts to extremely bright PhD graduates from another"
    "discipline who understand a lot of basic concepts but do not have a "
    "firm grasp on calculus and linear algebra. Please format your output in"
    "markdown format"
)
thinking = {"type": "disabled", "budget_tokens": 200}


# create function to create chat interface
def create_chat_interface(
    model: str,
    max_tokens: int,
    temperature: float,
    system: str,
    thinking: Optional[Union[str, Dict[str, Any]]] = {"type": "disabled"},
):
    # Initialize the Anthropic client
    client = anthropic.Anthropic()

    # Store conversation history
    messages: List[Dict[str, Any]] = []

    print("\n=== Claude Chat Interface ===")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        # Get user input
        user_input = input("\nYou: ")

        # Check for exit command
        if user_input.lower() in ["exit", "quit"]:
            print("\nEnding conversation. Goodbye!")
            break

        # Add user message to history
        messages.append(
            {"role": "user", "content": [{"type": "text", "text": user_input}]}
        )

        print("\nClaude is thinking...")

        try:
            # Get response from Claude
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                thinking=thinking,
                messages=messages,
            )

            # Extract the response text
            assistant_message = response.content[0].text

            # Add assistant's response to history
            messages.append(
                {
                    "role": "assistant",
                    "content": [{"type": "text", "text": assistant_message}],
                }
            )

            # Display the response with nice formatting
            print("\nClaude:")

            # display response with markdown format 
            console.print(Markdown(assistant_message))


        except Exception as e:
            print(f"\nAn error occurred: {e}")

    # return the output so can play with after
    return messages


if __name__ == "__main__":
    message_log = create_chat_interface(model, max_tokens, temperature, system)

    response = message_log[1]['content'][0]['text']
