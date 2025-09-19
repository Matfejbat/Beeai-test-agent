"""Hello World BeeAI Agent

A simple demonstration agent that greets users and echoes their messages.
This agent follows the BeeAI Hello World tutorial implementation.
"""

import asyncio
from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Context, Server, RunYield, RunYieldResume
from acp_sdk.utils.message_utils import get_message_text

# Create server instance
server = Server()


@server.agent(
    name="hello-world-agent",
    description="A friendly Hello World agent that greets users and echoes their messages"
)
async def hello_world_agent(
    input: list[Message], context: Context
) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    A simple Hello World agent implementation.
    
    Args:
        input: List of A2A Messages from the user
        context: Context object with run details (task_id, context_id, etc.)
    
    Yields:
        Message objects or string responses
    """
    # Extract text from the message
    user_message = get_message_text(input)
    
    # Yield a simple string response first
    yield f"Hello! You said: '{user_message}'"
    
    # Add a small delay for demonstration
    await asyncio.sleep(0.5)
    
    # Yield a more detailed response as a Message object
    yield Message(
        role="agent",
        parts=[MessagePart(
            content=f"Welcome to BeeAI! I'm your Hello World agent. I received your message and I'm ready to help. Your message was: {user_message}",
            content_type="text/plain"
        )]
    )


# Run the server when this script is executed directly
if __name__ == "__main__":
    server.run()
