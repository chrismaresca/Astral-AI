from __future__ import annotations
# ------------------------------------------------------------------------------
# Provider Agnostic Completions Response Models
# ------------------------------------------------------------------------------

"""
Provider Agnostic Completions Response Models
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# Built-in imports
from typing import List, Optional, Generic, Any
from typing_extensions import Literal

# Pydantic
from pydantic import BaseModel

# Base Resource Response
from ._base_resource_response import BaseProviderResourceResponse

# OpenAI
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.chat.chat_completion_token_logprob import ChatCompletionTokenLogprob

# TODO: Remove this once the openai types are updated
from openai._models import GenericModel

# Generic Types
from typing import TypeVar

StructuredOutputResponse = TypeVar("StructuredOutputResponse", bound=BaseModel)

# ------------------------------------------------------------------------------
# Choice Logprobs
# ------------------------------------------------------------------------------


class ChoiceLogprobs(BaseModel):
    content: Optional[List[ChatCompletionTokenLogprob]] = None
    """A list of message content tokens with log probability information."""

    refusal: Optional[List[ChatCompletionTokenLogprob]] = None
    """A list of message refusal tokens with log probability information."""


# ------------------------------------------------------------------------------
# Choice
# ------------------------------------------------------------------------------

class Choice(BaseModel):
    finish_reason: Literal["stop", "length", "tool_calls", "content_filter", "function_call"]
    """The reason the model stopped generating tokens.

    This will be `stop` if the model hit a natural stop point or a provided stop
    sequence, `length` if the maximum number of tokens specified in the request was
    reached, `content_filter` if content was omitted due to a flag from our content
    filters, `tool_calls` if the model called a tool, or `function_call`
    (deprecated) if the model called a function.
    """

    index: int
    """The index of the choice in the list of choices."""

    logprobs: Optional[ChoiceLogprobs] = None
    """Log probability information for the choice."""

    message: ChatCompletionMessage
    """A chat completion message generated by the model."""

# ------------------------------------------------------------------------------
# Chat Completion
# ------------------------------------------------------------------------------


class ChatCompletionResponse(BaseProviderResourceResponse):
    id: str
    """A unique identifier for the chat completion."""

    choices: List[Choice]
    """A list of chat completion choices.

    Can be more than one if `n` is greater than 1.
    """

    created: int
    """The Unix timestamp (in seconds) of when the chat completion was created."""

    model: str
    """The model used for the chat completion."""

    object: Literal["chat.completion"]
    """The object type, which is always `chat.completion`."""

    service_tier: Optional[Literal["scale", "default"]] = None
    """The service tier used for processing the request."""

    system_fingerprint: Optional[str] = None
    """This fingerprint represents the backend configuration that the model runs with.

    Can be used in conjunction with the `seed` request parameter to understand when
    backend changes have been made that might impact determinism.
    """


# ------------------------------------------------------------------------------
# Parsed Chat Completion Message
# ------------------------------------------------------------------------------

class ParsedChatCompletionMessage(ChatCompletionMessage, GenericModel, Generic[StructuredOutputResponse]):
    parsed: Optional[StructuredOutputResponse] = None
    """The auto-parsed message contents"""

    # TODO: Improve over time
    tool_calls: Optional[List[Any]] = None
    """The tool calls generated by the model, such as function calls."""


# ------------------------------------------------------------------------------
# Parsed Choice
# ------------------------------------------------------------------------------

class ParsedChoice(Choice, GenericModel, Generic[StructuredOutputResponse]):
    message: ParsedChatCompletionMessage[StructuredOutputResponse]
    """A chat completion message generated by the model."""


# ------------------------------------------------------------------------------
# Structured Output Completion Response
# ------------------------------------------------------------------------------

class StructuredOutputCompletionResponse(ChatCompletionResponse, GenericModel, Generic[StructuredOutputResponse]):
    """
    Structured Output Completion Response

    A provider-agnostic completion response that contains structured output
    in the form of a Pydantic model specified by the StructuredOutputResponse type parameter.
    """
    choices: List[ParsedChoice[StructuredOutputResponse]]
    """A list of structured output choices with parsed content."""
