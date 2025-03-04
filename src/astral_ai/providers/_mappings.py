from typing import Dict, Optional, overload, Literal
import threading
import json
import uuid

# Astral imports
from astral_ai._types import AstralClientParams
from astral_ai.constants._models import ModelProvider
from astral_ai._auth import AUTH_CONFIG_TYPE
from astral_ai.exceptions import ProviderNotSupportedError

# Provider imports
from astral_ai.providers._base_client import BaseProviderClient
from astral_ai.providers.anthropic import AnthropicProviderClient
from astral_ai.providers.openai import OpenAIProviderClient

# Adapter imports
from astral_ai.providers._base_adapters import BaseCompletionAdapter
from astral_ai.providers.openai._adapters import OpenAICompletionAdapter
from astral_ai.providers.anthropic._adapters import AnthropicCompletionAdapter

# -------------------------------------------------------------------------------- #
# Provider Adapter Mapping
# -------------------------------------------------------------------------------- #

_PROVIDER_ADAPTER_MAP: Dict[ModelProvider, BaseCompletionAdapter] = {
    "openai": OpenAICompletionAdapter,
    "anthropic": AnthropicCompletionAdapter,
}

# -------------------------------------------------------------------------------- #
# Adapter Registry
# -------------------------------------------------------------------------------- #

class AdapterRegistry:
    """
    Thread-safe registry for provider adapters.

    This registry lazily instantiates and caches adapters for each provider. All
    operations on the registry are synchronized using a reentrant lock to protect
    against concurrent access in multi-threaded environments.
    """

    _adapter_cache: Dict[ModelProvider, BaseCompletionAdapter] = {}
    _lock = threading.RLock()

    @overload
    @classmethod
    def get_adapter(cls, model_provider: Literal["openai", "azureOpenAI"]) -> OpenAICompletionAdapter:
        ...

    @overload
    @classmethod
    def get_adapter(cls, model_provider: Literal["anthropic"]) -> AnthropicCompletionAdapter:
        ...

    @classmethod
    def get_adapter(cls, model_provider: ModelProvider) -> BaseCompletionAdapter:
        """
        Retrieve the adapter for the given model provider in a thread-safe manner.
        If the adapter is not yet cached, it will be instantiated using _PROVIDER_ADAPTER_MAP.
        """
        with cls._lock:
            adapter = cls._adapter_cache.get(model_provider)
            if adapter is None:
                try:
                    adapter = _PROVIDER_ADAPTER_MAP[model_provider]()
                    cls._adapter_cache[model_provider] = adapter
                except KeyError:
                    raise ProviderNotSupportedError(provider_name=model_provider)
            return adapter

    @classmethod
    def register_adapter(cls, model_provider: ModelProvider, adapter: BaseCompletionAdapter) -> None:
        """
        Register or replace an adapter for the given model provider in a thread-safe manner.
        """
        with cls._lock:
            cls._adapter_cache[model_provider] = adapter

    @classmethod
    def unregister_adapter(cls, model_provider: ModelProvider) -> None:
        """
        Unregister the adapter for the given model provider in a thread-safe manner.
        """
        with cls._lock:
            if model_provider in cls._adapter_cache:
                del cls._adapter_cache[model_provider]

    @classmethod
    def clear_cache(cls) -> None:
        """
        Clear the entire adapter cache in a thread-safe manner.
        Any subsequent get_adapter() call will create a new instance.
        """
        with cls._lock:
            cls._adapter_cache.clear()

    @classmethod
    def get_all_adapters(cls) -> Dict[ModelProvider, BaseCompletionAdapter]:
        """
        Return a shallow copy of all registered adapters in a thread-safe manner.
        """
        with cls._lock:
            return dict(cls._adapter_cache)

    @classmethod
    def get_adapter_count(cls) -> int:
        """
        Return the number of registered adapters in a thread-safe manner.
        """
        with cls._lock:
            return len(cls._adapter_cache)

    @classmethod
    def get_adapter_by_index(cls, index: int) -> BaseCompletionAdapter:
        """
        Retrieve an adapter by its index in the cache in a thread-safe manner.
        Raises IndexError if the index is out of bounds.
        """
        with cls._lock:
            values = list(cls._adapter_cache.values())
            if index < 0 or index >= len(values):
                raise IndexError("Adapter index out of range")
            return values[index]

# -------------------------------------------------------------------------------- #
# Provider Client Registry
# -------------------------------------------------------------------------------- #

# Map of provider names to their client classes
_PROVIDER_CLIENT_MAP: Dict[ModelProvider, type[BaseProviderClient]] = {
    "openai": OpenAIProviderClient,
    "anthropic": AnthropicProviderClient,
}

class ProviderClientRegistry:
    """
    Thread-safe registry for provider clients.

    Clients are cached by a key derived either from an explicit unique client_key
    (if provided) or from the provider name and its authentication config.
    
    - When new_client is False (default), the key is generated deterministically.
    - When new_client is True:
      - The user must supply a unique client_key.
    """
    _client_registry: Dict[str, BaseProviderClient] = {}
    _lock = threading.RLock()

    @classmethod
    def _generate_registry_key(
        cls,
        provider_name: ModelProvider,
        config: Optional[AUTH_CONFIG_TYPE],
        client_key: Optional[str] = None,
    ) -> str:
        """
        Generate a key based on the provider name and auth configuration.

        If client_key is provided, it is used verbatim.
        Otherwise, if a config is provided, the key is generated from the provider name
        and a hash of the JSON representation of the config (with sorted keys).
        If neither is provided, the provider name is used.
        """
        if client_key:
            return client_key
        if config is not None:
            config_str = json.dumps({k: v.model_dump() for k, v in config.items()}, sort_keys=True)
            config_hash = hash(config_str)
            return f"{provider_name}_{config_hash}"
        return provider_name

    @overload
    @classmethod
    def get_client(
        cls,
        provider_name: Literal["openai", "azureOpenAI"],
        astral_client: Optional[AstralClientParams] = None,
    ) -> OpenAIProviderClient:
        ...

    @overload
    @classmethod
    def get_client(
        cls,
        provider_name: Literal["anthropic"],
        astral_client: Optional[AstralClientParams] = None,
    ) -> AnthropicProviderClient:
        ...

    @classmethod
    def get_client(
        cls,
        provider_name: ModelProvider,
        astral_client: Optional[AstralClientParams] = None,
    ) -> BaseProviderClient:
        """
        Retrieve the provider client for the given provider name and authentication configuration.

        - If astral_client is None, uses the default (cached) client for that provider.
        - If astral_client.new_client is True:
            - The user must supply a unique client_key; otherwise, a ValueError is raised.
        - Otherwise, a deterministic key is generated from provider name and client_config,
          and the cached client is returned if present.
        """
        if astral_client is None:
            key = cls._generate_registry_key(provider_name, None)
        else:
            if astral_client.new_client:
                if astral_client.client_key:
                    key = astral_client.client_key
                else:
                    raise ValueError(
                        "When new_client is True, you must provide a unique client_key."
                    )
            else:
                key = cls._generate_registry_key(provider_name, astral_client.client_config, astral_client.client_key)

        with cls._lock:
            if key not in cls._client_registry:
                client_class = _PROVIDER_CLIENT_MAP.get(provider_name)
                if client_class is None:
                    raise ProviderNotSupportedError(provider_name=provider_name)
                cls._client_registry[key] = client_class(astral_client.client_config if astral_client else None)
            return cls._client_registry[key]

    @classmethod
    def register_client(
        cls,
        provider_name: ModelProvider,
        client: BaseProviderClient,
        client_config: Optional[AUTH_CONFIG_TYPE] = None,
        client_key: Optional[str] = None,
    ) -> None:
        """
        Manually register or replace a provider client.
        """
        key = cls._generate_registry_key(provider_name, client_config, client_key)
        with cls._lock:
            cls._client_registry[key] = client

    @classmethod
    def unregister_client(
        cls,
        provider_name: ModelProvider,
        client_config: Optional[AUTH_CONFIG_TYPE] = None,
        client_key: Optional[str] = None,
    ) -> None:
        """
        Unregister a provider client.
        """
        key = cls._generate_registry_key(provider_name, client_config, client_key)
        with cls._lock:
            if key in cls._client_registry:
                del cls._client_registry[key]

    @classmethod
    def clear_cache(cls) -> None:
        """
        Clear the entire client cache.
        """
        with cls._lock:
            cls._client_registry.clear()

    @classmethod
    def get_all_clients(cls) -> Dict[str, BaseProviderClient]:
        """
        Return a shallow copy of all registered clients.
        """
        with cls._lock:
            return dict(cls._client_registry)

    @classmethod
    def get_client_count(cls) -> int:
        """
        Return the number of registered clients.
        """
        with cls._lock:
            return len(cls._client_registry)

    @classmethod
    def get_client_by_index(cls, index: int) -> BaseProviderClient:
        """
        Get the client at the given index.
        Raises IndexError if the index is out of range.
        """
        with cls._lock:
            values = list(cls._client_registry.values())
            if index < 0 or index >= len(values):
                raise IndexError("Client index out of range")
            return values[index]

    @classmethod
    def get_client_by_name(cls, name: str) -> BaseProviderClient:
        """
        Retrieve the client by its registry key.
        """
        with cls._lock:
            return cls._client_registry[name]
