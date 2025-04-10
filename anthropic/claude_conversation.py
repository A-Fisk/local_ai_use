import anthropic
import os
import textwrap
import json
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from rich.console import Console
from rich.markdown import Markdown
import pdb

# create console object for printing pretty markdown
console = Console()

# define model parameters
model = "claude-3-7-sonnet-latest"
max_tokens = 20000
temperature = 1
system = (
    "You are a world class mathematician and coder, you are helping to"
    "explain concepts to extremely bright PhD graduates from another"
    "discipline who understand a lot of basic concepts but do not have a "
    "firm grasp on calculus and linear algebra. Please format your output in"
    "markdown format, but the result will be output in a terminal so avoid "
    "using latex equations . "
    "Please use the correct english spelling for all outputs,"
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

    # Ask if user wants to modify the system prompt
    modify_prompt = input(
        "Would you like to modify the system prompt? (yes/no): "
    ).lower()
    if modify_prompt in ["yes", "y"]:
        print("\nCurrent system prompt:")
        print(system)
        print(
            "\n---- Enter your modified system prompt. Press CTRL+D to send:"
        )

        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass

        new_system = "\n".join(lines)
        if new_system.strip():  # Only update if not empty
            system = new_system
            print("\nSystem prompt updated.")
        else:
            print("\nSystem prompt unchanged.")

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
            print("\n--------- Claude:")

            # display output if enabled
            if thinking["type"] == "enabled":
                print("\n----- thinking:")
                console.print(assistant_thinking)
                print("\n----- responding:")

            # display response with markdown format
            console.print(Markdown(assistant_message))

        except Exception as e:
            print(f"\nAn error occurred: {e}")

    # return the output so can play with after
    return messages, thinking_output


def save_conversation_log(messages, thinking_log, system, model):
    """Save the conversation to a log file in the local_ai_use/logs directory."""
    # Determine the base project directory (local_ai_use) no matter where script is run from
    current_path = Path(os.path.abspath(__file__))
    # Navigate to the project root directory
    while (
        current_path.name != "local_ai_use"
        and current_path.parent != current_path
    ):
        current_path = current_path.parent

    # If we couldn't find "local_ai_use" directory, default to current directory
    if current_path.name != "local_ai_use":
        current_path = Path.cwd()
        print(
            f"Warning: 'local_ai_use' directory not found. Using current directory: {current_path}"
        )

    # Create logs directory in the project root
    logs_dir = current_path / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Create a timestamp for the filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Extract model name for the filename (remove version details)
    model_name = model.split("-")[0:3]
    model_name = "-".join(model_name)

    # Extract the first user message and get just the first three words
    first_user_msg = ""
    for msg in messages:
        if msg["role"] == "user":
            # Get first three words from the message
            words = msg["content"][0]["text"].split()
            first_three = words[:3] if len(words) >= 3 else words
            first_user_msg = "_".join(first_three)
            break

    # Count the number of message exchanges (an exchange is a user message followed by an assistant response)
    num_exchanges = len([msg for msg in messages if msg["role"] == "user"])

    # Create a filename with the timestamp, model name, first three words, and conversation length
    sanitized_title = "".join(
        c if c.isalnum() or c in "_-" else "_" for c in first_user_msg
    )
    filename = (
        f"{timestamp}_{model_name}_{sanitized_title}_{num_exchanges}msgs.json"
    )
    log_path = logs_dir / filename

    # Create the log data
    log_data = {
        "timestamp": timestamp,
        "model": model,
        "system": system,
        "messages": messages,
        "thinking": thinking_log if thinking_log else [],
    }

    # Save to file
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    return log_path


if __name__ == "__main__":
    message_log, thinking_log = create_chat_interface(
        model, max_tokens, temperature, system, thinking
    )

    # Save the conversation log
    if message_log:
        log_path = save_conversation_log(
            message_log, thinking_log, system, model
        )
        print(f"\nConversation saved to: {log_path}")

    # debugging output
    if message_log and len(message_log) > 1:
        response = message_log[1]["content"][0]["text"]
