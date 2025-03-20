import anthropic
import os
import textwrap
from typing import List, Dict, Any, Optional, Union
from rich.console import Console
from rich.markdown import Markdown
import pdb

# create console object for printing pretty markdown
console = Console()

# define model parameters
model = "claude-3-7-sonnet-latest"
max_tokens = 5000
temperature = 1
system = (
    "You are a world class mathematician and coder, you are helping to"
    "explain concepts to extremely bright PhD graduates from another"
    "discipline who understand a lot of basic concepts but do not have a "
    "firm grasp on calculus and linear algebra. Please format your output in"
    "markdown format. Please use the correct english spelling for all outputs,"
    " such as colour and maths"
)
thinking = {"type": "enabled", "budget_tokens": 2000}


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
    thinking_output = []

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

            # capture thinking traces if present
            if thinking["type"] == "enabled":
                # Extract the response text
                assistant_message = response.content[1].text

                # extract thinking
                assistant_thinking = response.content[0].thinking
                thinking_output.append(assistant_thinking)

            else:
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

            # display output if enabled 
            if thinking["type"] == "enabled":
                print("\nthinking:")
                console.print(assistant_thinking)
                print("\nresponding:")

            # display response with markdown format
            console.print(Markdown(assistant_message))

        except Exception as e:
            print(f"\nAn error occurred: {e}")

    # return the output so can play with after
    return messages, thinking_output


if __name__ == "__main__":
    message_log, thinking_log = create_chat_interface(
        model, max_tokens, temperature, system, thinking
    )

    # debugging output 
    response = message_log[1]["content"][0]["text"]
