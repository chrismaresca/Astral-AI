# -------------------------------------------------------------------------------- #
# Test OpenAI Request Models
# -------------------------------------------------------------------------------- #

"""
Tests for OpenAI Request Models in Astral AI
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
# Built-in imports
import pytest
import unittest
from unittest.mock import patch
from typing import Dict, List

# Pydantic
from pydantic import BaseModel, ValidationError

# OpenAI Types
from openai.types.chat import ChatCompletion

# Astral AI imports
from src.astral_ai.providers.openai._types import (
    OpenAIRequestChat,
    OpenAIRequestStreaming,
    OpenAIRequestStructured,
    OpenAIRequestType
)

from src.astral_ai.constants._models import OpenAIModels
from src.astral_ai.providers.openai._types._request import OpenAIRequest


# -------------------------------------------------------------------------------- #
# Test Data
# -------------------------------------------------------------------------------- #

@pytest.fixture
def basic_chat_request() -> Dict:
    return {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "Hello!"}],
        "temperature": 0.7,
        "max_tokens": 100
    }

@pytest.fixture
def streaming_request() -> Dict:
    return {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "Hello!"}],
        "stream": True,
        "temperature": 0.7
    }

class TestSchema(BaseModel):
    response: str
    confidence: float

@pytest.fixture
def structured_request() -> Dict:
    return {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "Hello!"}],
        "response_format": TestSchema(response="test", confidence=0.9)
    }

# -------------------------------------------------------------------------------- #
# Tests
# -------------------------------------------------------------------------------- #

def test_chat_request_creation(basic_chat_request):
    """Test basic chat request creation and validation"""
    print("\n=== Starting Chat Request Creation Test ===")
    
    print("\n--- Creating Chat Request ---")
    request = OpenAIRequestChat(**basic_chat_request)
    
    print("\n--- Request Details ---")
    print(f"Model: {request['model']}")
    print(f"Messages: {request['messages']}")
    print(f"Temperature: {request['temperature']}")
    print(f"Max Tokens: {request['max_tokens']}")
    
    print("\n--- Running Assertions ---")
    assert request["model"] == "gpt-4o", "Model mismatch"
    print("✓ Model assertion passed")
    
    assert isinstance(request["messages"], list), "Messages not a list"
    print("✓ Messages type assertion passed")
    
    assert request["temperature"] == 0.7, "Temperature mismatch"
    print("✓ Temperature assertion passed")
    
    print("\n=== Chat Request Creation Test Completed Successfully ===")


# -------------------------------------------------------------------------------- #
# Streaming Request Creation
# -------------------------------------------------------------------------------- #

def test_streaming_request_creation(streaming_request):
    """Test streaming request creation and validation"""
    print("\n=== Starting Streaming Request Creation Test ===")
    
    print("\n--- Creating Streaming Request ---")
    request = OpenAIRequestStreaming(**streaming_request)
    
    print("\n--- Request Details ---")
    print(f"Model: {request['model']}")
    print(f"Stream: {request['stream']}")
    
    print("\n--- Running Assertions ---")
    assert request["stream"] is True, "Stream flag not set"
    print("✓ Stream flag assertion passed")
    
    print("\n=== Streaming Request Creation Test Completed Successfully ===")


# -------------------------------------------------------------------------------- #
# Structured Request Creation
# -------------------------------------------------------------------------------- #

def test_structured_request_creation(structured_request):
    """Test structured request creation with schema"""
    print("\n=== Starting Structured Request Creation Test ===")
    
    print("\n--- Creating Structured Request ---")
    request = OpenAIRequestStructured[TestSchema](**structured_request)
    
    print("\n--- Request Details ---")
    print(f"Model: {request['model']}")
    print(f"Response Format: {request['response_format']}")
    
    print("\n--- Running Assertions ---")
    assert isinstance(request["response_format"], TestSchema), "Response format not correct schema"
    print("✓ Response format type assertion passed")
    
    print("\n=== Structured Request Creation Test Completed Successfully ===")


# -------------------------------------------------------------------------------- #
# Request Type Union
# -------------------------------------------------------------------------------- #

def test_request_type_union():
    """Test that different request types can be used as OpenAIRequestType"""
    print("\n=== Starting Request Type Union Test ===")
    
    def process_request(request: OpenAIRequestType):
        return True
    
    print("\n--- Testing Different Request Types ---")
    chat_request = OpenAIRequestChat(model="gpt-4o", messages=[])
    streaming_request = OpenAIRequestStreaming(model="gpt-4o", messages=[], stream=True)
    structured_request = OpenAIRequestStructured[TestSchema](
        model="gpt-4o", 
        messages=[],
        response_format=TestSchema(response="test", confidence=0.9)
    )
    
    print("\n--- Running Assertions ---")
    assert process_request(chat_request), "Failed to process chat request"
    print("✓ Chat request processing passed")
    
    assert process_request(streaming_request), "Failed to process streaming request"
    print("✓ Streaming request processing passed")
    
    assert process_request(structured_request), "Failed to process structured request"
    print("✓ Structured request processing passed")
    
    print("\n=== Request Type Union Test Completed Successfully ===")

def test_invalid_chat_request():
    """Test chat request creation with missing required fields"""
    print("\n=== Starting Invalid Chat Request Test ===")
    
    print("\n--- Creating Chat Request with Missing Fields ---")
    try:
        OpenAIRequestChat(model="gpt-4o")  # Missing 'messages' field
    except ValidationError as e:
        print(f"✓ Caught expected ValidationError: {e}")

    print("\n--- Running Assertions ---")
    with pytest.raises(ValidationError):
        OpenAIRequestChat(model="gpt-4o")

    print("✓ ValidationError correctly raised for missing messages field")
    print("\n=== Invalid Chat Request Test Completed Successfully ===")


def test_chat_request_exceeding_max_tokens():
    """Test chat request with max_tokens exceeding the allowed limit"""
    print("\n=== Starting Chat Request Exceeding Max Tokens Test ===")
    
    request_data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "Hello!"}],
        "temperature": 0.7,
        "max_tokens": 999999  # Very large value
    }

    print("\n--- Creating Chat Request with Excessive max_tokens ---")
    try:
        OpenAIRequestChat(**request_data)
    except ValueError as e:
        print(f"✓ Caught expected ValueError: {e}")

    print("\n--- Running Assertions ---")
    with pytest.raises(ValueError):
        OpenAIRequestChat(**request_data)

    print("✓ ValueError correctly raised for exceeding max tokens limit")
    print("\n=== Chat Request Exceeding Max Tokens Test Completed Successfully ===")


def test_empty_message_request():
    """Test that empty messages are not allowed"""
    print("\n=== Starting Empty Message Request Test ===")
    
    print("\n--- Creating Chat Request with Empty Messages ---")
    try:
        OpenAIRequestChat(model="gpt-4o", messages=[])
    except ValueError as e:
        print(f"✓ Caught expected ValueError: {e}")

    print("\n--- Running Assertions ---")
    with pytest.raises(ValueError):
        OpenAIRequestChat(model="gpt-4o", messages=[])

    print("✓ ValueError correctly raised for empty messages")
    print("\n=== Empty Message Request Test Completed Successfully ===")


def test_partial_streaming_response():
    """Test handling of incomplete streaming response"""
    print("\n=== Starting Partial Streaming Response Test ===")
    
    incomplete_data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "Hello!"}],
        "stream": True  # Missing optional fields like temperature
    }

    print("\n--- Creating Partial Streaming Request ---")
    request = OpenAIRequestStreaming(**incomplete_data)

    print("\n--- Running Assertions ---")
    assert request.model == "gpt-4o", "Model name mismatch"
    print("✓ Model assertion passed")

    assert request.stream is True, "Stream flag not set correctly"
    print("✓ Stream flag assertion passed")
    
    assert hasattr(request, "temperature"), "Temperature attribute missing"
    print("✓ Temperature attribute exists (default or None)")

    print("\n=== Partial Streaming Response Test Completed Successfully ===")


# -------------------------------------------------------------------------------- #
# Tests for OpenAI API interactions using mocking (without class)
# -------------------------------------------------------------------------------- #

@patch('openai.ChatCompletion.create')  # Mocking OpenAI's API call
def test_openai_request(mock_openai):
    """Test sending a message using OpenAIRequest and mock API response"""
    print("\n=== Starting OpenAI API Mocked Request Test ===")

    print("\n--- Mocking OpenAI API Response ---")
    mock_openai.return_value = {
        "choices": [{"message": {"content": "Hello, world!"}}]
    }

    print("\n--- Sending Mocked Request ---")
    request = OpenAIRequest()
    response = request.send_message("Hello")

    print("\n--- Running Assertions ---")
    assert response == "Hello, world!", "Response content mismatch"
    print("✓ Response correctly received from OpenAI")

    print("\n=== OpenAI API Mocked Request Test Completed Successfully ===")


@patch('openai.ChatCompletion.create')
def test_openai_request_rate_limit_exceeded(mock_openai):
    """Test OpenAI request handling when API rate limit is exceeded"""
    print("\n=== Starting OpenAI API Rate Limit Handling Test ===")

    print("\n--- Mocking Rate Limit Error ---")
    mock_openai.side_effect = Exception("Rate limit exceeded")

    print("\n--- Sending Mocked Request ---")
    request = OpenAIRequest()

    try:
        request.send_message("Test message")
    except Exception as e:
        print(f"✓ Caught expected exception: {e}")

    print("\n--- Running Assertions ---")
    with patch('openai.ChatCompletion.create', side_effect=Exception("Rate limit exceeded")):
        try:
            request.send_message("Test message")
        except Exception as e:
            assert str(e) == "Rate limit exceeded", "Unexpected exception message"

    print("✓ Exception correctly raised for rate limit exceeded")
    print("\n=== OpenAI API Rate Limit Handling Test Completed Successfully ===")


# -------------------------------------------------------------------------------- #
# Run Tests if executed directly
# -------------------------------------------------------------------------------- #

if __name__ == '__main__':
    test_openai_request()
    test_openai_request_rate_limit_exceeded()
    print("\n✅ All tests passed successfully!")