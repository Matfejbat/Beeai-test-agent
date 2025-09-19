"""Tests for the Enhanced BeeAI Agent

This module contains unit tests for the enhanced agent functionality
including input validation, intent analysis, and error handling.
"""

import pytest
import asyncio
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Context
from unittest.mock import Mock

# Import functions from our agent
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'beeai_agents'))
from agent import validate_input, extract_user_intent


class TestInputValidation:
    """Test cases for input validation functionality."""
    
    def test_validate_input_with_valid_messages(self):
        """Test validation with valid input messages."""
        messages = [
            Message(
                role="user",
                parts=[MessagePart(content="Hello, world!", content_type="text/plain")]
            )
        ]
        assert validate_input(messages) is True
    
    def test_validate_input_with_empty_list(self):
        """Test validation with empty message list."""
        assert validate_input([]) is False
    
    def test_validate_input_with_empty_parts(self):
        """Test validation with messages that have no parts."""
        messages = [Message(role="user", parts=[])]
        assert validate_input(messages) is False
    
    def test_validate_input_with_empty_content(self):
        """Test validation with empty content."""
        messages = [
            Message(
                role="user",
                parts=[MessagePart(content="", content_type="text/plain")]
            )
        ]
        assert validate_input(messages) is False
    
    def test_validate_input_with_non_string_content(self):
        """Test validation with non-string content."""
        messages = [
            Message(
                role="user",
                parts=[MessagePart(content=123, content_type="text/plain")]
            )
        ]
        assert validate_input(messages) is False


class TestIntentAnalysis:
    """Test cases for intent analysis functionality."""
    
    def test_extract_user_intent_basic(self):
        """Test basic intent extraction."""
        result = extract_user_intent("Hello, how are you?")
        assert result["message"] == "Hello, how are you?"
        assert result["intent"] == "general_chat"
        assert result["contains_question"] is True
        assert result["is_greeting"] is True
        assert result["is_farewell"] is False
        assert result["word_count"] == 4
    
    def test_extract_user_intent_greeting(self):
        """Test intent extraction for greetings."""
        greetings = ["Hello", "Hi there", "Good morning", "Hey"]
        for greeting in greetings:
            result = extract_user_intent(greeting)
            assert result["is_greeting"] is True
            assert result["is_farewell"] is False
    
    def test_extract_user_intent_farewell(self):
        """Test intent extraction for farewells."""
        farewells = ["Goodbye", "Bye", "See you later", "Take care"]
        for farewell in farewells:
            result = extract_user_intent(farewell)
            assert result["is_farewell"] is True
            assert result["is_greeting"] is False
    
    def test_extract_user_intent_positive_sentiment(self):
        """Test sentiment analysis for positive messages."""
        positive_messages = [
            "This is great!",
            "I love this agent",
            "Awesome work!",
            "Excellent functionality"
        ]
        for message in positive_messages:
            result = extract_user_intent(message)
            assert result["sentiment"] == "positive"
    
    def test_extract_user_intent_negative_sentiment(self):
        """Test sentiment analysis for negative messages."""
        negative_messages = [
            "This is terrible",
            "I hate this",
            "Awful experience",
            "Bad implementation"
        ]
        for message in negative_messages:
            result = extract_user_intent(message)
            assert result["sentiment"] == "negative"
    
    def test_extract_user_intent_neutral_sentiment(self):
        """Test sentiment analysis for neutral messages."""
        neutral_messages = [
            "What is the weather?",
            "Can you help me?",
            "Show me the documentation",
            "How does this work?"
        ]
        for message in neutral_messages:
            result = extract_user_intent(message)
            assert result["sentiment"] == "neutral"
    
    def test_extract_user_intent_question_detection(self):
        """Test question detection."""
        questions = [
            "What is your name?",
            "How are you?",
            "Can you help me?",
            "Is this working?"
        ]
        for question in questions:
            result = extract_user_intent(question)
            assert result["contains_question"] is True
        
        statements = [
            "This is a statement.",
            "I like this agent",
            "Great work",
            "Hello there"
        ]
        for statement in statements:
            result = extract_user_intent(statement)
            assert result["contains_question"] is False
    
    def test_extract_user_intent_word_count(self):
        """Test word count calculation."""
        test_cases = [
            ("Hello", 1),
            ("Hello world", 2),
            ("This is a longer message", 5),
            ("How are you doing today?", 5)
        ]
        for message, expected_count in test_cases:
            result = extract_user_intent(message)
            assert result["word_count"] == expected_count


class TestEdgeCases:
    """Test cases for edge cases and error scenarios."""
    
    def test_extract_user_intent_empty_string(self):
        """Test intent extraction with empty string."""
        result = extract_user_intent("")
        assert result["message"] == ""
        assert result["word_count"] == 1  # split("") returns [""]
        assert result["contains_question"] is False
        assert result["is_greeting"] is False
        assert result["is_farewell"] is False
    
    def test_extract_user_intent_only_punctuation(self):
        """Test intent extraction with only punctuation."""
        result = extract_user_intent("?!@#$%")
        assert result["contains_question"] is True
        assert result["sentiment"] == "neutral"
    
    def test_extract_user_intent_mixed_case(self):
        """Test intent extraction with mixed case."""
        result = extract_user_intent("HELLO there!")
        assert result["is_greeting"] is True
    
    def test_extract_user_intent_multiple_sentiments(self):
        """Test intent extraction with conflicting sentiments."""
        # Equal positive and negative words should result in neutral
        result = extract_user_intent("I love this but I also hate that")
        assert result["sentiment"] == "neutral"


if __name__ == "__main__":
    pytest.main([__file__])
