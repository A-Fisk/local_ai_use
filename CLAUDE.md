# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment
- Use conda environment `ai_env` defined in environment.yml
- Key packages: anthropic, openai, black, rich

## Build/Lint/Test Commands
- Format code: `black .`
- Run linting: `black --check .`
- Run a specific Python file: `python path/to/file.py`

## Code Style Guidelines
- Line length: 79 characters (black configured)
- Imports: group standard library, third-party, and local imports
- Do not use typing annotations for function parameters and returns
- Error handling: use try/except blocks with specific exception types
- Markdown formatting for Claude outputs (rich.markdown)
- Use British English spelling (colour, maths)
- Use textwrap for multiline strings
- Format system prompts with clear instructions
