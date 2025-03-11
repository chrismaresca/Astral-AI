# -------------------------------------------------------------------------------- #
# Test OpenAI Response Models
# -------------------------------------------------------------------------------- #

"""
Tests for OpenAI Response Models in Astral AI
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
# Built-in imports
import pytest
from unittest.mock import patch
from typing import Dict, List

# Pydantic
from pydantic import BaseModel

# OpenAI Types
from openai.types.chat import ChatCompletion, ChatCompletionChunk

# Astral AI imports
from src.astral_ai.providers.openai._types import (
    OpenAIChatResponseType,
    OpenAIStreamingResponseType,
    OpenAIStructuredResponseType,
    OpenAIResponseType
)
from src.astral_ai.providers.openai._types._response import OpenAIResponse
# -------------------------------------------------------------------------------- #
# Test Data
# -------------------------------------------------------------------------------- #

@pytest.fixture
def chat_completion_data() -> Dict:
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-4o-01-15-24",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hello! How can I help you today?"
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 9,
            "completion_tokens": 12,
            "total_tokens": 21
        }
    }

@pytest.fixture
def streaming_chunk_data() -> Dict:
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion.chunk",
        "created": 1677652288,
        "model": "gpt-4o-01-15-24",
        "choices": [{
            "index": 0,
            "delta": {
                "content": "Hello"
            },
            "finish_reason": None
        }]
    }

class TestSchema(BaseModel):
    response: str
    confidence: float

# -------------------------------------------------------------------------------- #
# Tests
# -------------------------------------------------------------------------------- #

def test_chat_response_handling(chat_completion_data):
    """Test handling of standard chat completion responses"""
    print("\n=== Starting Chat Response Handling Test ===")
    
    print("\n--- Creating Chat Response ---")
    response: OpenAIChatResponseType = ChatCompletion(**chat_completion_data)
    
    print("\n--- Response Details ---")
    print(f"ID: {response.id}")
    print(f"Model: {response.model}")
    print(f"Choices: {response.choices}")
    print(f"Usage: {response.usage}")
    
    print("\n--- Running Assertions ---")
    assert response.id == "chatcmpl-123", "Response ID mismatch"
    print("✓ Response ID assertion passed")
    
    assert response.model == "gpt-4o-01-15-24", "Model mismatch"
    print("✓ Model assertion passed")
    
    assert len(response.choices) == 1, "Incorrect number of choices"
    print("✓ Choices length assertion passed")
    
    print("\n=== Chat Response Handling Test Completed Successfully ===")

def test_streaming_response_handling(streaming_chunk_data):
    """Test handling of streaming response chunks"""
    print("\n=== Starting Streaming Response Handling Test ===")
    
    print("\n--- Creating Streaming Response Chunk ---")
    chunk: OpenAIStreamingResponseType = ChatCompletionChunk(**streaming_chunk_data)
    
    print("\n--- Chunk Details ---")
    print(f"ID: {chunk.id}")
    print(f"Object: {chunk.object}")
    print(f"Choices: {chunk.choices}")
    
    print("\n--- Running Assertions ---")
    assert chunk.object == "chat.completion.chunk", "Incorrect object type"
    print("✓ Object type assertion passed")
    
    assert chunk.choices[0].delta.content == "Hello", "Incorrect chunk content"
    print("✓ Chunk content assertion passed")
    
    print("\n=== Streaming Response Handling Test Completed Successfully ===")

def test_structured_response_handling():
    """Test handling of structured responses with schema"""
    print("\n=== Starting Structured Response Handling Test ===")
    
    print("\n--- Creating Structured Response Data ---")
    structured_data = {
        "response": "test response",
        "confidence": 0.95
    }
    
    print("\n--- Creating Structured Response ---")
    response = TestSchema(**structured_data)
    
    print("\n--- Response Details ---")
    print(f"Response: {response.response}")
    print(f"Confidence: {response.confidence}")
    
    print("\n--- Running Assertions ---")
    assert response.response == "test response", "Response content mismatch"
    print("✓ Response content assertion passed")
    
    assert response.confidence == 0.95, "Confidence value mismatch"
    print("✓ Confidence value assertion passed")
    
    print("\n=== Structured Response Handling Test Completed Successfully ===")


@pytest.mark.usefixtures("chat_completion_data", "streaming_chunk_data")
def test_response_type_union():
    """Test that different response types can be used as OpenAIResponseType"""
    print("\n=== Starting Response Type Union Test ===")

    def process_response(response: OpenAIResponseType):
        return True

    # Get fixture data
    chat_data = chat_completion_data()
    stream_data = streaming_chunk_data()

    print("\n--- Creating Different Response Types ---")
    chat_response = ChatCompletion(**chat_data)
    streaming_response = ChatCompletionChunk(**stream_data)

    print("\n--- Running Assertions ---")
    assert process_response(chat_response), "Failed to process chat response"
    print("✓ Chat response processing passed")

    assert process_response(streaming_response), "Failed to process streaming response"
    print("✓ Streaming response processing passed")

    print("\n=== Response Type Union Test Completed Successfully ===")

# -------------------------------------------------------------------------------- #
# Additional Tests for OpenAIResponse
# -------------------------------------------------------------------------------- #

@patch('openai.ChatCompletion.create')  # Mock OpenAI API call
def test_mocked_openai_response(mock_openai):
    """Test that OpenAIResponse correctly parses an API response"""
    print("\n=== Starting OpenAI API Mocked Response Test ===")

    mock_openai.return_value = {
        "choices": [{"message": {"content": "Test OpenAI response"}}]
    }

    response_handler = OpenAIResponse()
    parsed_response = response_handler.parse(mock_openai.return_value)

    print("\n--- Running Assertions ---")
    assert parsed_response == "Test OpenAI response", "Response parsing failed"

    print("✓ OpenAI API Mocked Response Test Passed")

def test_empty_response_handling():
    """Test handling of empty API responses"""
    print("\n=== Starting Empty Response Handling Test ===")

    response_handler = OpenAIResponse()
    empty_response = {"choices": []}

    print("\n--- Running Assertions ---")
    assert response_handler.parse(empty_response) == "", "Empty response should return an empty string"

    print("✓ Empty Response Handling Test Passed")

def test_invalid_response_handling():
    """Test handling of invalid or malformed responses"""
    print("\n=== Starting Invalid Response Handling Test ===")

    response_handler = OpenAIResponse()
    malformed_response = {"unexpected_key": "data"}  # Missing 'choices' key

    print("\n--- Running Assertions ---")
    try:
        response_handler.parse(malformed_response)
        assert False, "Expected KeyError but none was raised"
    except KeyError:
        print("✓ Invalid Response Handling Test Passed")

def test_partial_response_handling():
    """Test handling of incomplete API responses"""
    print("\n=== Starting Partial Response Handling Test ===")

    response_handler = OpenAIResponse()
    partial_response = {"choices": [{"message": {}}]}  # Missing 'content' key

    print("\n--- Running Assertions ---")
    assert response_handler.parse(partial_response) == "", "Partial response should return an empty string"

    print("✓ Partial Response Handling Test Passed")

if __name__ == '__main__':
    print("\n✅ All tests should be run using pytest. Example:")
    print("   pytest -s test_response.py")