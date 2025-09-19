"""Enhanced Hello World BeeAI Agent

A demonstration agent with improved functionality including error handling,
logging, input validation, and enhanced response capabilities.
This agent follows BeeAI best practices and ACP protocol standards.
"""

import asyncio
import logging
from collections.abc import AsyncGenerator
from typing import Optional
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Context, Server, RunYield, RunYieldResume
from acp_sdk.utils.message_utils import get_message_text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
server = Server()


def validate_input(messages: list[Message]) -> bool:
    """
    Validate input messages to ensure they contain valid content.
    
    Args:
        messages: List of input messages to validate
        
    Returns:
        bool: True if input is valid, False otherwise
    """
    if not messages:
        return False
    
    for message in messages:
        if not message.parts:
            return False
        for part in message.parts:
            if not part.content or not isinstance(part.content, str):
                return False
    
    return True


def extract_user_intent(user_message: str) -> dict:
    """
    Simple intent extraction to demonstrate enhanced functionality.
    
    Args:
        user_message: The user's input message
        
    Returns:
        dict: Intent analysis result
    """
    user_message_lower = user_message.lower()
    
    intent_analysis = {
        "message": user_message,
        "intent": "general_chat",
        "sentiment": "neutral",
        "contains_question": "?" in user_message,
        "is_greeting": any(greeting in user_message_lower for greeting in 
                          ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"]),
        "is_farewell": any(farewell in user_message_lower for farewell in 
                          ["bye", "goodbye", "farewell", "see you", "take care"]),
        "word_count": len(user_message.split())
    }
    
    # Simple sentiment analysis
    positive_words = ["good", "great", "awesome", "wonderful", "excellent", "love", "like"]
    negative_words = ["bad", "terrible", "awful", "hate", "dislike", "horrible"]
    
    positive_count = sum(1 for word in positive_words if word in user_message_lower)
    negative_count = sum(1 for word in negative_words if word in user_message_lower)
    
    if positive_count > negative_count:
        intent_analysis["sentiment"] = "positive"
    elif negative_count > positive_count:
        intent_analysis["sentiment"] = "negative"
    
    return intent_analysis


@server.agent(
    name="enhanced-hello-world-agent",
    description="An enhanced Hello World agent with error handling, logging, input validation, and basic intent analysis"
)
async def enhanced_hello_world_agent(
    input: list[Message], context: Context
) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    Enhanced Hello World agent with improved functionality.
    
    Args:
        input: List of A2A Messages from the user
        context: Context object with run details (task_id, context_id, etc.)
    
    Yields:
        Message objects or string responses with enhanced features
    """
    try:
        # Log the incoming request
        logger.info(f"Received request with {len(input)} messages in context {context.context_id}")
        
        # Validate input
        if not validate_input(input):
            logger.warning("Invalid input received")
            yield "I'm sorry, but I received invalid input. Please send me a text message!"
            return
        
        # Extract text from the message
        user_message = get_message_text(input)
        logger.info(f"Processing message: '{user_message[:50]}...' (truncated)")
        
        # Perform intent analysis
        yield {"thought": "Analyzing user intent and sentiment..."}
        await asyncio.sleep(0.3)
        
        intent_analysis = extract_user_intent(user_message)
        
        # Generate personalized greeting based on intent
        if intent_analysis["is_greeting"]:
            greeting_response = "Hello there! It's wonderful to meet you! 👋"
        elif intent_analysis["is_farewell"]:
            greeting_response = "Goodbye! It was great chatting with you! 👋"
        elif intent_analysis["contains_question"]:
            greeting_response = f"I see you have a question! You asked: '{user_message}'"
        else:
            greeting_response = f"Hello! You said: '{user_message}'"
        
        # Add sentiment response
        if intent_analysis["sentiment"] == "positive":
            greeting_response += " I can sense the positive energy in your message! ✨"
        elif intent_analysis["sentiment"] == "negative":
            greeting_response += " I hope I can help brighten your day! 🌟"
        
        yield greeting_response
        
        # Add a processing delay for demonstration
        yield {"thought": "Preparing detailed response..."}
        await asyncio.sleep(0.5)
        
        # Generate enhanced response with analysis
        enhanced_response = Message(
            role="agent",
            parts=[MessagePart(
                content=f"""Welcome to the Enhanced BeeAI Agent! 🤖

**Message Analysis:**
• Intent: {intent_analysis['intent']}
• Sentiment: {intent_analysis['sentiment']}
• Word count: {intent_analysis['word_count']}
• Contains question: {'Yes' if intent_analysis['contains_question'] else 'No'}
• Is greeting: {'Yes' if intent_analysis['is_greeting'] else 'No'}

**Your message:** "{user_message}"

I'm an enhanced version of the Hello World agent with additional capabilities like input validation, intent analysis, and error handling. I'm ready to help you explore BeeAI's capabilities!

**What I can do:**
• Analyze sentiment and intent
• Validate input messages
• Provide detailed responses
• Handle errors gracefully
• Log interactions for debugging

Feel free to send me another message to see how I respond! 🚀""",
                content_type="text/plain"
            )]
        )
        
        yield enhanced_response
        
        # Log successful completion
        logger.info(f"Successfully processed request in context {context.context_id}")
        
    except Exception as e:
        # Enhanced error handling
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        yield Message(
            role="agent",
            parts=[MessagePart(
                content=f"I apologize, but I encountered an error while processing your request: {str(e)}. Please try again or contact support if the issue persists.",
                content_type="text/plain"
            )]
        )


# Health check endpoint functionality
@server.agent(
    name="health-check",
    description="Simple health check agent to verify system status"
)
async def health_check_agent(
    input: list[Message], context: Context
) -> AsyncGenerator[RunYield, RunYieldResume]:
    """Simple health check agent for monitoring."""
    yield Message(
        role="agent",
        parts=[MessagePart(
            content="✅ Agent is healthy and operational! System status: OK",
            content_type="text/plain"
        )]
    )


# Run the server when this script is executed directly
if __name__ == "__main__":
    logger.info("Starting Enhanced BeeAI Agent Server...")
    server.run()
