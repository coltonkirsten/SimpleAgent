# SimpleAgentFramework

A lightweight, modular framework for building AI agents with various LLM backends including OpenAI and Anthropic.

## Features

- Support for multiple LLM providers (OpenAI, Anthropic) via LiteLLM
- Extensible tool system for agent capabilities
- Built-in logging
- Streaming and non-streaming response modes
- Simple interface for quick prototyping

## Setup

### Installation

1. Clone the repository

   ```
   git clone https://github.com/yourusername/SimpleAgentFramework.git
   cd SimpleAgentFramework
   ```

2. Set up a virtual environment

   ```
   python3 -m venv .venv
   ```

3. Activate the virtual environment

   ```
   # On macOS/Linux
   source ./venv_manager.sh on

   # On Windows
   .venv\Scripts\activate
   ```

4. Install dependencies

   ```
   pip install -r requirements.txt
   ```

5. Set up your API keys (create a `.env` file in the root directory)
   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

## Usage

### Basic Usage

The simplest way to test the framework is to run the test agent:

```python
python test_agent.py
```

This will start an interactive chat session with the agent.

### Adding Custom Tools

Create new tools in the `tools` directory following the pattern in existing tools.

## Available Tools

- Weather information
- Web search
- Light control (demo)
- Utility tools
- Programming tools
