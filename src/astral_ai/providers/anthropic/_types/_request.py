from __future__ import annotations
# ------------------------------------------------------------------------------
# Anthropic Request Models
# ------------------------------------------------------------------------------

"""
Anthropic Request Models for Astral AI
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------

# Built-in

from typing import (Literal,
                    Optional,
                    Dict,
                    List,
                    Iterable,
                    Union,
                    TypedDict,
                    Required,
                    TypeAlias,
                    TypeVar,
                    Generic,
                    NotRequired)

# HTTPX Timeout
from httpx import Timeout

# Pydantic
from pydantic import BaseModel

# Astral AI
from astral_ai.constants._models import AnthropicModels

# OpenAI Types
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionChunk, ParsedChatCompletion, ChatCompletion

# Astral AI Types
from astral_ai._types._request._request import (
    ToolChoice,
    ReasoningEffort,
    ResponseFormat,
    Metadata,
    ResponsePrediction,
    Modality,
    StreamOptions,
    Tool,
)

# OpenAI Types
from ._message import AnthropicMessageType
# ------------------------------------------------------------------------------
# Generic Types
# ------------------------------------------------------------------------------

# Response Format Type
_ResponseFormatT = TypeVar("ResponseFormatT", bound=BaseModel)


# ------------------------------------------------------------------------------
# OpenAI Request Objects
# ------------------------------------------------------------------------------


class AnthropicRequestBase(TypedDict):
    """
    Anthropic Request Base Model for Astral AI
    """
    model: Required[AnthropicModels]
    messages: Required[AnthropicMessageType]
    max_tokens: NotRequired[int]

    # frequency_penalty: NotRequired[float]
    # """Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far."""

    # logit_bias: Optional[Dict[str, int]]
    # """Modify the likelihood of specified tokens appearing in the completion."""

    # logprobs: Optional[bool]
    # """Whether to return log probabilities of the output tokens."""

    # max_completion_tokens: Optional[int]
    # """An upper bound for the number of tokens that can be generated for a completion."""

    # max_tokens: Optional[int]
    # """The maximum number of tokens that can be generated in the chat completion (deprecated in favor of `max_completion_tokens`)."""

    # metadata: Optional[Metadata]
    # """Set of key-value pairs that can be attached to the object (max 16 pairs)."""

    # modalities: Optional[List[Modality]]
    # """Output types that you would like the model to generate for this request (e.g., ['text'] or ['text', 'audio'])."""

    # n: Optional[int]
    # """How many chat completion choices to generate for each input message."""

    # parallel_tool_calls: Optional[bool]
    # """Whether to enable parallel function calling during tool use."""

    # prediction: Optional[ResponsePrediction]
    # """Static predicted output content (e.g., content of a text file being regenerated)."""

    # presence_penalty: Optional[float]
    # """Number between -2.0 and 2.0. Positive values penalize tokens based on whether they appear in the text so far."""

    # reasoning_effort: Optional[ReasoningEffort]
    # """For reasoning models only. Constrains effort on reasoning (e.g., 'low', 'medium', 'high')."""

    # response_format: Optional[ResponseFormat]
    # """Specifies the format that the model must output."""

    # seed: Optional[int]
    # """If specified, attempts to make sampling deterministic for repeated requests."""

    # service_tier: Optional[Literal["auto", "default"]]
    # """Specifies the latency tier to use for processing the request."""

    # stop: Optional[Union[str, List[str]]]
    # """Up to 4 sequences where the API will stop generating further tokens."""

    # store: Optional[bool]
    # """Whether or not to store the output of this chat completion request."""

    # stream_options: Optional[StreamOptions]
    # """Options for streaming responses; only set when `stream` is true."""

    # temperature: Optional[float]
    # """Sampling temperature to use, between 0 and 2."""

    # tool_choice: Optional[ToolChoice]
    # """Controls which (if any) tool is called by the model."""

    # tools: Optional[Iterable[Tool]]
    # """A list of tools the model may call (e.g., functions)."""

    # top_logprobs: Optional[int]
    # """An integer (0 to 20) specifying the number of most likely tokens to return at each token position."""

    # top_p: Optional[float]
    # """Nucleus sampling parameter, where the model considers tokens with top_p probability mass."""

    # user: Optional[str]
    # """A unique identifier representing your end-user."""

    # timeout: Optional[Union[float, Timeout]]
    # """Override the client-level default timeout for this request (in seconds)."""


# ------------------------------------------------------------------------------
# Chat Request
# ------------------------------------------------------------------------------

class AnthropicRequestChat(AnthropicRequestBase, total=False):
    pass

# ------------------------------------------------------------------------------
# OpenAI Request Types
# ------------------------------------------------------------------------------


class AnthropicRequestStreaming(AnthropicRequestBase):
    stream: Literal[True]

# ------------------------------------------------------------------------------
# OpenAI Request Types
# ------------------------------------------------------------------------------s


class AnthropicRequestStructured(Generic[_ResponseFormatT], AnthropicRequestBase):
    response_format: _ResponseFormatT


# ------------------------------------------------------------------------------
# OpenAI Type Aliases
# ------------------------------------------------------------------------------

# Chat Request
AnthropicRequestChatType: TypeAlias = AnthropicRequestChat

# Streaming Request
AnthropicRequestStreamingType: TypeAlias = AnthropicRequestStreaming

# Structured Request
AnthropicRequestStructuredType: TypeAlias = AnthropicRequestStructured

# Union of all request types
AnthropicRequestType: TypeAlias = Union[AnthropicRequestChatType, AnthropicRequestStreamingType, AnthropicRequestStructuredType]


# ------------------------------------------------------------------------------
# TODO: Anthropic Embedding Request Types
# ------------------------------------------------------------------------------

class AnthropicRequestEmbedding(AnthropicRequestBase, total=False):
    pass


AnthropicRequestEmbeddingType: TypeAlias = AnthropicRequestEmbedding
