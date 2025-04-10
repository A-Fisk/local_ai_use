import json
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
import argparse

# Create console object for printing pretty markdown
console = Console()


def find_logs_directory():
    """Find the logs directory within the local_ai_use project."""
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

    # Return logs directory in the project root
    logs_dir = current_path / "logs"
    if not logs_dir.exists():
        print(f"Error: Logs directory not found at {logs_dir}")
        sys.exit(1)

    return logs_dir


def list_log_files(logs_dir):
    """List all log files in the logs directory with numbers for selection."""
    log_files = sorted(
        logs_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True
    )

    if not log_files:
        print("No log files found.")
        sys.exit(1)

    print("\n=== Available Log Files ===")
    for i, log_file in enumerate(log_files, 1):
        print(f"{i}. {log_file.name}")

    return log_files


def view_log(log_path):
    """Display the contents of a log file in markdown format."""
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            log_data = json.load(f)

        # Display log information
        print("\n=== Log Information ===")
        print(f"Timestamp: {log_data['timestamp']}")
        print(f"Model: {log_data['model']}")
        print("\nSystem Prompt:")
        print(log_data["system"])

        # Display messages with thinking interleaved
        print("\n=== Conversation ===")
        thinking_index = 0
        thinking_traces = log_data.get("thinking", [])
        
        for i, msg in enumerate(log_data["messages"]):
            role = msg["role"]
            if role == "user":
                print("\n----- User:")
                print(msg["content"][0]["text"])
            elif role == "assistant":
                # Show thinking trace before assistant response if available
                if thinking_index < len(thinking_traces) and i > 0 and log_data["messages"][i-1]["role"] == "user":
                    print("\n----- Thinking:")
                    console.print(thinking_traces[thinking_index])
                    thinking_index += 1
                
                print("\n----- Claude:")
                console.print(Markdown(msg["content"][0]["text"]))
        
        # Display any remaining thinking traces
        while thinking_index < len(thinking_traces):
            print(f"\n----- Thinking (unmatched {thinking_index + 1}):")
            console.print(thinking_traces[thinking_index])
            thinking_index += 1

    except Exception as e:
        print(f"Error reading log file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="View Claude conversation logs in markdown format."
    )
    parser.add_argument(
        "log_file", nargs="?", help="Path to the log file (optional)"
    )
    args = parser.parse_args()

    # Find the logs directory
    logs_dir = find_logs_directory()

    if args.log_file:
        # Use the provided log file path
        log_path = Path(args.log_file)
        if not log_path.exists():
            # Try to find it in the logs directory
            log_path = logs_dir / args.log_file
            if not log_path.exists():
                print(f"Error: Log file not found: {args.log_file}")
                sys.exit(1)
    else:
        # List available log files and let user select one
        log_files = list_log_files(logs_dir)

        while True:
            try:
                selection = input(
                    "\nEnter the number of the log file to view (or 'q' to quit): "
                )
                if selection.lower() in ["q", "quit", "exit"]:
                    sys.exit(0)

                idx = int(selection) - 1
                if 0 <= idx < len(log_files):
                    log_path = log_files[idx]
                    break
                else:
                    print(
                        f"Invalid selection. Please enter a number between 1 and {len(log_files)}."
                    )
            except ValueError:
                print("Please enter a valid number.")

    # View the selected log file
    view_log(log_path)


if __name__ == "__main__":
    main()
