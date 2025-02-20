# ------------------------------------------------------------------------------
# Request Models
# ------------------------------------------------------------------------------

"""
Request Models for Astral AI
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# Built-in
from typing import (Literal,
                    Optional,
                    Dict,
                    List,
                    Iterable,
                    Union,
                    TypeAlias,
                    Any,
                    TypedDict,
                    Required,
                    TypeVar)

# Abstract Base Classes
from abc import ABC

# Standard Library
import time
import uuid

# Typing Extensions
from typing_extensions import Self

# Pydantic
from pydantic import BaseModel, Field, model_validator, PrivateAttr, ConfigDict

# HTTPX Timeout
from httpx import Timeout

# Message Models
from astral_ai.messaging import Message, MessageList

# Astral AI
from astral_ai.constants._models import ModelName, ModelProvider, get_provider_from_model_name

# Astral AI Types
from astral_ai._types._base import NotGiven, NOT_GIVEN

# Astral AI Types
from astral_ai._types._astral import AstralParams

# ------------------------------------------------------------------------------
# Modality
# ------------------------------------------------------------------------------


Modality: TypeAlias = Optional[Literal["text", "audio"]]


# ------------------------------------------------------------------------------
# Stream Options
# ------------------------------------------------------------------------------

class StreamOptions(TypedDict, total=False):
    include_usage: bool
    """If set, an additional chunk will be streamed before the `data: [DONE]` message.

    The `usage` field on this chunk shows the token usage statistics for the entire
    request, and the `choices` field will always be an empty array. All other chunks
    will also include a `usage` field, but with a null value.
    """


# ------------------------------------------------------------------------------
# Reasoning Effort
# ------------------------------------------------------------------------------
ReasoningEffort: TypeAlias = Optional[Literal["low", "medium", "high"]]


# ------------------------------------------------------------------------------
# Response Format
# ------------------------------------------------------------------------------


class ResponseFormatJSONSchema(TypedDict, total=False):
    type: Required[Literal["json_schema"]]
    json_schema: Required[Dict[str, Any]]


class ResponseFormatJSONObject(TypedDict, total=False):
    type: Required[Literal["json_object"]]


class ResponseFormatText(TypedDict, total=False):
    type: Required[Literal["text"]]


ResponseFormat: TypeAlias = Union[ResponseFormatText, ResponseFormatJSONObject, ResponseFormatJSONSchema]


# ------------------------------------------------------------------------------
# Tools
# ------------------------------------------------------------------------------


class ToolDefinition(TypedDict, total=False):
    name: Required[str]
    """The name of the function to be called.

    Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length
    of 64.
    """

    description: str
    """
    A description of what the function does, used by the model to choose when and
    how to call the function.
    """

    parameters: Dict[str, object]
    """The parameters the functions accepts, described as a JSON Schema object.

    See the [guide](https://platform.openai.com/docs/guides/function-calling) for
    examples, and the
    [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for
    documentation about the format.

    Omitting `parameters` defines a function with an empty parameter list.
    """

    strict: Optional[bool]
    """Whether to enable strict schema adherence when generating the function call.

    If set to true, the model will follow the exact schema defined in the
    `parameters` field. Only a subset of JSON Schema is supported when `strict` is
    `true`. Learn more about Structured Outputs in the
    [function calling guide](docs/guides/function-calling).
    """


class Tool(TypedDict, total=False):
    function: Required[ToolDefinition]
    """The function to call."""

    type: Required[Literal["function"]]
    """The type of the tool. Currently, only `function` is supported."""


# ------------------------------------------------------------------------------
# Tool Choice
# ------------------------------------------------------------------------------


class ToolAlias(TypedDict, total=True):
    name: Required[str]
    """The name of the tool to call."""


class SpecificToolSelection(TypedDict, total=False):
    function: Required[ToolAlias]

    type: Required[Literal["function"]]
    """The type of the tool. Currently, only `function` is supported."""


ToolChoice: TypeAlias = Union[
    Literal["none", "auto", "required"], SpecificToolSelection
]


# ------------------------------------------------------------------------------
# Prediction Content
# ------------------------------------------------------------------------------


class TextContentPart(TypedDict, total=False):
    text: Required[str]
    """The text content."""

    type: Required[Literal["text"]]
    """The type of the content part."""


class ResponsePrediction(TypedDict, total=False):
    content: Required[Union[str, Iterable[TextContentPart]]]
    """
    The content that should be matched when generating a model response. If
    generated tokens would match this content, the entire model response can be
    returned much more quickly.
    """

# ------------------------------------------------------------------------------
# Metadata
# ------------------------------------------------------------------------------


Metadata: TypeAlias = Dict[str, str]


# ------------------------------------------------------------------------------
# Base Request
# ------------------------------------------------------------------------------

class BaseRequest(BaseModel, ABC):
    """
    Base Request for Astral AI
    """

    _request_id: str = PrivateAttr(default_factory=lambda: str(uuid.uuid4()))
    _time_created: float = PrivateAttr(default_factory=lambda: time.time())
    _provider_name: ModelProvider = PrivateAttr()

    # Model
    model: ModelName = Field(description="The model to use for the request.")

    # Astral Parameters
    astral_params: AstralParams = Field(default_factory=AstralParams, description="Astral parameters.")

    @property
    def request_id(self) -> str:
        """The request ID for the request."""
        return self._request_id

    @property
    def provider_name(self) -> ModelProvider:
        """The provider name for the request."""
        return self._provider_name

    @model_validator(mode="after")
    def set_provider_name(self) -> Self:
        """Set the provider name for the request."""
        self._provider_name = get_provider_from_model_name(model_name=self.model)
        return self


# ------------------------------------------------------------------------------
# Astral Completion Request
# ------------------------------------------------------------------------------

class AstralCompletionRequest(BaseRequest):
    """
    Astral Completion Request
    """

    # Messages
    messages: Union[MessageList, List[Message], Message] = Field(description="The messages to send to the model.")

    # Stream
    stream: bool = Field(default=False, description="If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a `data: [DONE]` message.")

    # TODO: Audio
    # audio: Optional[AudioParam] | NotGiven = Field(default=NOT_GIVEN, description="Parameters for audio output. Required when audio output is requested with `modalities: ['audio']`.")

    # Frequency Penalty
    frequency_penalty: Optional[float] | NotGiven = Field(default=NOT_GIVEN, description="Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.")

    # Logit Bias
    logit_bias: Optional[Dict[str, int]] | NotGiven = Field(default=NOT_GIVEN, description="Modify the likelihood of specified tokens appearing in the completion. Accepts a JSON object that maps tokens (specified by their token ID in the tokenizer) to an associated bias value from -100 to 100. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.")

    # Logprobs
    logprobs: Optional[bool] | NotGiven = Field(default=NOT_GIVEN, description="Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the `content` of `message`.")

    # Max Completion Tokens
    max_completion_tokens: Optional[int] | NotGiven = Field(default=NOT_GIVEN, description="An upper bound for the number of tokens that can be generated for a completion, including visible output tokens and reasoning tokens.")

    # Max Tokens
    max_tokens: Optional[int] | NotGiven = Field(default=NOT_GIVEN, description="The maximum number of tokens that can be generated in the chat completion. This value can be used to control costs for text generated via API. This value is now deprecated in favor of `max_completion_tokens`, and is not compatible with o1 series models.")

    # Metadata
    metadata: Optional[Metadata] | NotGiven = Field(default=NOT_GIVEN, description="Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.")

    # Modality
    modalities: Optional[List[Modality]] | NotGiven = Field(default=NOT_GIVEN, description="Output types that you would like the model to generate for this request. Most models are capable of generating text, which is the default: `['text']`. The `gpt-4o-audio-preview` model can also be used to generate audio. To request that this model generate both text and audio responses, you can use: `['text', 'audio']`")

    # Number of Completions
    n: Optional[int] | NotGiven = Field(default=NOT_GIVEN, description="How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep `n` as `1` to minimize costs.")

    # Allow Parallel Tool Calls
    parallel_tool_calls: bool | NotGiven = Field(default=NOT_GIVEN, description="Whether to enable parallel function calling during tool use.")

    # Prediction
    prediction: Optional[ResponsePrediction] | NotGiven = Field(default=NOT_GIVEN, description="Static predicted output content, such as the content of a text file that is being regenerated.")

    # Presence Penalty
    presence_penalty: Optional[float] | NotGiven = Field(default=NOT_GIVEN, description="Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.")

    # Reasoning Effort
    reasoning_effort: ReasoningEffort | NotGiven = Field(default=NOT_GIVEN, description="o1 and o3-mini models only. Constrains effort on reasoning for reasoning models. Currently supported values are `low`, `medium`, and `high`. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response.")

    # Response Format
    response_format: ResponseFormat | NotGiven = Field(default=NOT_GIVEN, description="An object specifying the format that the model must output. Setting to `{ 'type': 'json_schema', 'json_schema': {...} }` enables Structured Outputs which ensures the model will match your supplied JSON schema. Setting to `{ 'type': 'json_object' }` enables JSON mode, which ensures the message the model generates is valid JSON.")

    # Seed
    seed: Optional[int] | NotGiven = Field(default=NOT_GIVEN, description="This feature is in Beta. If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result. Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend.")

    # Service Tier
    service_tier: Optional[Literal["auto", "default"]] | NotGiven = Field(default=NOT_GIVEN, description="Specifies the latency tier to use for processing the request. This parameter is relevant for customers subscribed to the scale tier service. If set to 'auto', and the Project is Scale tier enabled, the system will utilize scale tier credits until they are exhausted. If set to 'auto', and the Project is not Scale tier enabled, the request will be processed using the default service tier with a lower uptime SLA and no latency guarantee.")

    # Stop
    stop: Union[Optional[str], List[str]] | NotGiven = Field(default=NOT_GIVEN, description="Up to 4 sequences where the API will stop generating further tokens.")

    # Store
    store: Optional[bool] | NotGiven = Field(default=NOT_GIVEN, description="Whether or not to store the output of this chat completion request for use in our model distillation or evals products.")

    # Stream Options
    stream_options: Optional[StreamOptions] | NotGiven = Field(default=NOT_GIVEN, description="Options for streaming response. Only set this when you set `stream: true`.")

    # Temperature
    temperature: Optional[float] | NotGiven = Field(default=NOT_GIVEN, description="What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both.")

    # TOOLS
    tool_choice: ToolChoice | NotGiven = Field(default=NOT_GIVEN, description="Controls which (if any) tool is called by the model. `none` means the model will not call any tool and instead generates a message. `auto` means the model can pick between generating a message or calling one or more tools. `required` means the model must call one or more tools. Specifying a particular tool via `{'type': 'function', 'function': {'name': 'my_function'}}` forces the model to call that tool.")
    tools: Iterable[Tool] | NotGiven = Field(default=NOT_GIVEN, description="A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for. A max of 128 functions are supported.")

    # Top Logprobs
    top_logprobs: Optional[int] | NotGiven = Field(default=NOT_GIVEN, description="An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. `logprobs` must be set to `true` if this parameter is used.")

    # Top P
    top_p: Optional[float] | NotGiven = Field(default=NOT_GIVEN, description="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.")

    # User
    user: str | NotGiven = Field(default=NOT_GIVEN, description="A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.")

    # Timeout
    timeout: float | Timeout | None | NotGiven = Field(default=NOT_GIVEN, description="Override the client-level default timeout for this request, in seconds")

    # --------------------------------------------------------------------------
    # Model Config
    # --------------------------------------------------------------------------

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # --------------------------------------------------------------------------
    # To Provider Dict
    # --------------------------------------------------------------------------

    def to_provider_dict(self) -> dict:
        """
        Convert the AstralCompletionRequest to a dict excluding unset fields and those set to NOT_GIVEN.
        """
        # Get fields explicitly provided by the user (or set to a default explicitly)
        raw = self.model_dump(exclude_unset=True)
        # Filter out any field with a value that is NOT_GIVEN
        return {key: value for key, value in raw.items() if value is not NOT_GIVEN}


# ------------------------------------------------------------------------------
# Astral Structured Completion Request
# ------------------------------------------------------------------------------

StructuredOutputResponseT = TypeVar('StructuredOutputResponseT', bound=BaseModel)


class AstralStructuredCompletionRequest(AstralCompletionRequest):
    """
    Astral Structured Completion Request
    """
    response_format: StructuredOutputResponseT = Field(description="The response format to use for the request.")

# ------------------------------------------------------------------------------
# Astral Embedding Request
# ------------------------------------------------------------------------------
