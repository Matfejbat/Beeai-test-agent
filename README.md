# BeeAI Test Agent

A simple Hello World agent built with the BeeAI Platform following the official tutorial. This agent demonstrates the basic structure and functionality of a BeeAI agent using the ACP (Agent Communication Protocol) SDK.

## Features

- Simple greeting functionality
- Message echoing
- Demonstrates basic BeeAI agent structure
- Uses ACP SDK for agent communication
- Follows BeeAI Hello World tutorial implementation

## Project Structure

```
beeai-test-agent/
├── src/beeai_agents/
│   ├── __init__.py          # Empty package file
│   └── agent.py             # Main agent implementation
├── Dockerfile               # Container configuration
├── pyproject.toml          # Dependencies and metadata
├── uv.lock                 # Dependency lock file (generated)
└── README.md               # This file
```

## Prerequisites

- [BeeAI Platform](https://docs.beeai.dev/introduction/quickstart) installed
- [uv](https://docs.astral.sh/uv/) package manager
- Python 3.11 or higher

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Matfejbat/Beeai-test-agent.git
cd Beeai-test-agent
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Start the server

```bash
uv run python -m beeai_agents.agent
```

The server will start on `http://localhost:8000`.

### 4. Test the agent (in another terminal)

```bash
# List available agents
beeai list

# Run the agent interactively
beeai run hello-world-agent "Hello, BeeAI!"
```

You should see the agent respond with a greeting and echo of your message.

## Agent Details

### Agent Function

The main agent function is decorated with `@server.agent()` and implements:

- **Name**: `hello-world-agent`
- **Description**: A friendly Hello World agent that greets users and echoes their messages
- **Input**: List of A2A Messages
- **Output**: Async generator yielding AgentMessage or string responses

### Key Features

- Uses `get_message_text()` to extract text from A2A Messages
- Demonstrates both string and AgentMessage response types
- Includes async operations with `asyncio.sleep()`
- Follows BeeAI Hello World tutorial structure

## Development

### Running Locally

```bash
# Install dependencies
uv sync

# Run the agent server
uv run python -m beeai_agents.agent
```

### Docker Support

```bash
# Build the Docker image
docker build -t beeai-test-agent .

# Run the container
docker run -p 8000:8000 beeai-test-agent
```

## Next Steps

Now that you have a working Hello World agent, you can:

- Explore [GUI configuration options](https://docs.beeai.dev/build-agents/agent-details) through AgentDetail
- Leverage [LLM Access](https://docs.beeai.dev/build-agents/llm-access) in your agent
- Learn about [Messages](https://docs.beeai.dev/build-agents/messages) for communication
- Build beautiful GUI with [GUI Components](https://docs.beeai.dev/build-agents/gui-components)
- Request structured input using [forms](https://docs.beeai.dev/build-agents/forms)
- Work with [files](https://docs.beeai.dev/build-agents/files)
- [Share your agent](https://docs.beeai.dev/how-to/share-agents) with others

## Resources

- [BeeAI Documentation](https://docs.beeai.dev/)
- [BeeAI Hello World Tutorial](https://docs.beeai.dev/build-agents/hello-world)
- [BeeAI Platform Agent Starter](https://github.com/i-am-bee/beeai-platform-agent-starter)
- [Agent Communication Protocol](https://agentcommunicationprotocol.dev/)

## License

MIT License - see the code for details.

## Contributing

Feel free to submit issues and pull requests to improve this test agent!
