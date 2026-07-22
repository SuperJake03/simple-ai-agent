# Simple AI Agent

A minimal, from-scratch AI coding agent written in Python, powered by Google's Gemini API. Give it a natural-language instruction and it plans and executes a sequence of function calls — listing files, reading file contents, writing files, and running Python scripts — inside a sandboxed working directory, looping until it produces a final response.

This project includes a small sample codebase (`calculator/`) as a sandbox for the agent to explore, read, and modify.

## Features

- **Agentic loop** — sends the user's prompt to Gemini, executes any requested function calls, feeds the results back, and repeats (up to 20 iterations) until the model returns a final text response
- **Function calling / tool use** — the agent has access to four tools:
  - `get_files_info` — list files/directories with size and type info
  - `get_file_content` — read a file's contents (truncated at a configurable max length)
  - `write_file` — write or overwrite a file
  - `run_python_file` — execute a Python file with optional arguments and capture its output
- **Sandboxed working directory** — every file operation is restricted to a configured working directory; any path that would escape it is rejected
- **Verbose mode** — optionally print token usage and detailed function call/response info for debugging

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended — this project includes a `uv.lock`)
- A [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key)

## Installation

Clone the repository:

```bash
git clone https://github.com/SuperJake03/simple-ai-agent.git
cd simple-ai-agent
```

Install dependencies with `uv`:

```bash
uv sync
```

Or with `pip`:

```bash
pip install google-genai==1.12.1 python-dotenv==1.1.0
```

Create a `.env` file in the project root with your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the agent with a prompt:

```bash
uv run main.py "your prompt here"
```

Add `--verbose` to see token usage and detailed function call/response logging:

```bash
uv run main.py "how many files are in the working directory?" --verbose
```

### Example

```bash
uv run main.py "What does the calculator app do? Look at the code and tell me."
```

The agent will use its tools to list files, read relevant source files in the sandboxed working directory, and respond with a summary — printing each function call it makes along the way.

## Configuration

Settings live in `config.py`:

| Setting | Description |
|---|---|
| `WORKING_DIR` | The directory the agent is sandboxed to (default: `./calculator`) |
| `MAX_CHARS` | Maximum number of characters read from a file before truncating (default: `10000`) |

The system prompt that defines the agent's behavior lives in `prompts.py`.

## Project structure

```
.
├── main.py                       # Entry point: runs the agent loop against the Gemini API
├── call_function.py              # Maps Gemini function calls to real Python functions and invokes them
├── config.py                      # Working directory and file-size limits
├── prompts.py                     # System prompt defining the agent's behavior
├── functions/
│   ├── get_files_info.py         # Tool: list files/directories
│   ├── get_file_content.py       # Tool: read file contents
│   ├── write_file.py             # Tool: write/overwrite a file
│   └── run_python_file.py        # Tool: execute a Python file
├── test_get_files_info.py         # Tests for each tool
├── test_get_file_content.py
├── test_write_file.py
├── test_run_python_file.py
├── calculator/                    # Sample sandboxed project the agent can operate on
│   ├── main.py                    # A simple expression calculator CLI
│   ├── tests.py
│   ├── lorem.txt
│   └── pkg/
│       ├── calculator.py          # Expression evaluation logic
│       ├── render.py              # Output formatting
│       └── morelorem.txt
├── pyproject.toml
└── uv.lock
```

## How it works

1. `main.py` sends the user's prompt to Gemini (`gemini-2.5-flash`), along with the system prompt and the available tool schemas.
2. If Gemini responds with one or more function calls, `call_function.py` looks up the matching Python function, injects the sandboxed `working_directory`, and executes it.
3. Every file-touching tool (`get_files_info`, `get_file_content`, `write_file`, `run_python_file`) independently verifies that the resolved absolute path stays within the working directory before doing anything, returning an error string instead of executing if it doesn't.
4. Function results are appended to the conversation and sent back to Gemini, and the loop repeats — allowing the agent to chain multiple tool calls (e.g. list files, then read one, then run it) — until Gemini returns a plain text response with no further function calls, or 20 iterations pass without one.

## Running tests

```bash
uv run python -m unittest discover
```
