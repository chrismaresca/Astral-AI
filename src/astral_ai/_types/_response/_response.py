from __future__ import annotations
# ------------------------------------------------------------------------------
# Response Models
# ------------------------------------------------------------------------------

"""
Response Models for Astral AI
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# Standard Library
import time
import uuid

# Types
from typing import Optional, Iterable, TypeVar, Generic

# Typed Extensions
from typing_extensions import Self

# Pydantic
from pydantic import BaseModel, PrivateAttr, Field, model_validator

# Astral AI
from astral_ai.constants._models import ModelName, ModelProvider

# Astral AI Utils
from astral_ai.utilities import get_provider_from_model_name

# Astral AI Types
from ._usage import (
    ChatUsage,
    ChatCost,
    BaseUsage,
    BaseCost,
)


# ------------------------------------------------------------------------------
# Provider Response and Message Objects
# ------------------------------------------------------------------------------


class ProviderResponseObject(BaseModel):
    """
    Provider Response Model for Astral AI
    """
    provider_object: str = Field(description="The object type of the provider response")
    provider_response_id: str = Field(description="The ID of the provider response")
    provider_model_id: str = Field(description="The ID of the provider model")
    provider_request_id: str = Field(description="The ID of the provider request")
    provider_created: int = Field(description="The created time (UNIX timestamp) for the provider response")


class ProviderResponseMessage(BaseModel):
    """
    Message Model for Astral AI
    """
    role: str = Field(description="The role of the message")
    content: str = Field(description="The content of the message")


class ProviderResponseMessageObject(BaseModel):
    """
    Message Object Model for Astral AI
    """
    index: int = Field(description="The index of the message")
    message: ProviderResponseMessage = Field(description="The message for the response")
    finish_reason: str = Field(description="The finish reason for the message")

# ------------------------------------------------------------------------------
# Base Response
# ------------------------------------------------------------------------------


class AstralBaseResponse(BaseModel):
    """
    Base Response Model for Astral AI
    """
    _response_id: str = PrivateAttr(default_factory=lambda: str(uuid.uuid4()))
    _time_created: float = PrivateAttr(default_factory=lambda: time.time())
    _provider_name: ModelProvider = PrivateAttr()

    # Model
    model: ModelName = Field(description="The model used to generate the response")

    # Provider Response
    provider_response: Optional[ProviderResponseObject] = Field(
        description="The provider response object", default=None
    )

    # Usage
    usage: BaseUsage = Field(description="The usage for the response")
    cost: Optional[BaseCost] = Field(description="The cost for the response", default=None)

    @property
    def response_id(self) -> str:
        """
        Get the response ID
        """
        return self._response_id

    @property
    def time_created(self) -> float:
        """
        Get the time created
        """
        return self._time_created

    @property
    def provider_name(self) -> ModelProvider:
        """
        Get the provider name
        """
        return self._provider_name

    @model_validator(mode="after")
    def set_provider_name(self) -> Self:
        """
        Set the provider name
        """
        self._provider_name = get_provider_from_model_name(self.model)
        return self

# ------------------------------------------------------------------------------
# Generic Mixin for Private Field Propagation
# ------------------------------------------------------------------------------


ResponseT = TypeVar('ResponseT', bound=AstralBaseResponse)
UsageT = TypeVar('UsageT', bound=BaseUsage)
CostT = TypeVar('CostT', bound=BaseCost)


class PrivatePropagationMixin(BaseModel, Generic[UsageT, CostT]):
    """
    Mixin to propagate private fields from a response to its usage.
    Assumes that the class has:
      - a 'usage' field with private attributes: _response_id, _model_provider, _model_name
      - properties 'response_id', 'provider_name', and 'model'
    """

    @model_validator(mode="after")
    def propagate_private_usage_fields(self: ResponseT) -> ResponseT:
        self.usage._response_id = self.response_id
        self.usage._model_provider = self.provider_name
        self.usage._model_name = self.model
        return self

    @model_validator(mode="after")
    def propagate_private_cost_fields(self: ResponseT) -> ResponseT:
        if self.cost is not None:
            self.cost._response_id = self.response_id
            self.cost._model_provider = self.provider_name
            self.cost._model_name = self.model
        return self


# ------------------------------------------------------------------------------
# Chat Response
# ------------------------------------------------------------------------------


class AstralChatResponse(PrivatePropagationMixin[ChatUsage, ChatCost], AstralBaseResponse):
    """
    Chat Response Model for Astral AI
    """
    response: str = Field(description="The response for the chat completion")
    usage: ChatUsage = Field(description="The usage for the response")
    cost: Optional[ChatCost] = Field(description="The cost for the response", default=None)

# ------------------------------------------------------------------------------
# AI Structured Response Objects
# ------------------------------------------------------------------------------


StructuredOutputResponse = TypeVar('StructuredOutputResponse', bound=BaseModel)

# ------------------------------------------------------------------------------
# Structured Response
# ------------------------------------------------------------------------------


class AstralStructuredResponse(AstralChatResponse, Generic[StructuredOutputResponse]):
    """
    Structured Response Model for Astral AI
    """
    response: StructuredOutputResponse = Field(description="The response for the structured response")
