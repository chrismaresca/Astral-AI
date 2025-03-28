from typing import Dict, Optional, overload, Literal
import threading
import json
import uuid

# Astral imports
from astral_ai._types import AstralClientParams
from astral_ai.constants._models import ModelProvider
from astral_ai._auth import AUTH_CONFIG_TYPE
from astral_ai.errors.exceptions import ProviderNotSupportedError

# Provider imports
from astral_ai.providers._base_client import BaseProviderClient
from astral_ai.providers.anthropic import AnthropicProviderClient
from astral_ai.providers.openai import OpenAIProviderClient
from astral_ai.providers.deepseek._client import DeepSeekProviderClient


# Map of provider names to their client classes
_PROVIDER_CLIENT_MAP: Dict[ModelProvider, type[BaseProviderClient]] = {
    "openai": OpenAIProviderClient,
    "anthropic": AnthropicProviderClient,
    "deepseek": DeepSeekProviderClient,
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
        async_client: bool = False,
    ) -> str:
        """
        Generate a key based on the provider name and auth configuration.

        If client_key is provided, it is used verbatim.
        Otherwise, if a config is provided, the key is generated from the provider name
        and a hash of the JSON representation of the config (with sorted keys).
        If neither is provided, the provider name is used.
        
        The key is suffixed with ".async" if async_client is True.
        """
        base_key = ""
        if client_key:
            base_key = client_key
        elif config is not None:
            config_str = json.dumps({k: v.model_dump() for k, v in config.items()}, sort_keys=True)
            config_hash = hash(config_str)
            base_key = f"{provider_name}_{config_hash}"
        else:
            base_key = provider_name
            
        # Add suffix for async clients
        return f"{base_key}.async" if async_client else base_key

    @overload
    @classmethod
    def get_client(
        cls,
        provider_name: Literal["openai", "azureOpenAI"],
        astral_client: Optional[AstralClientParams] = None,
        async_client: bool = False,
    ) -> OpenAIProviderClient:
        ...

    @overload
    @classmethod
    def get_client(
        cls,
        provider_name: Literal["anthropic"],
        astral_client: Optional[AstralClientParams] = None,
        async_client: bool = False,
    ) -> AnthropicProviderClient:
        ...

    @overload
    @classmethod
    def get_client(
        cls,
        provider_name: Literal["deepseek"],
        astral_client: Optional[AstralClientParams] = None,
        async_client: bool = False,
    ) -> DeepSeekProviderClient:
        ...
        
    @classmethod
    def get_client(
        cls,
        provider_name: ModelProvider,
        astral_client: Optional[AstralClientParams] = None,
        async_client: bool = False,
    ) -> BaseProviderClient:
        """
        Retrieve the provider client for the given provider name and authentication configuration.

        - If astral_client is None, uses the default (cached) client for that provider.
        - If astral_client.new_client is True:
            - The user must supply a unique client_key; otherwise, a ValueError is raised.
        - Otherwise, a deterministic key is generated from provider name and client_config,
          and the cached client is returned if present.
          
        Args:
            provider_name: The name of the provider to get a client for
            astral_client: Optional client parameters
            async_client: Whether to return an async client (default: False)
        """
        if astral_client is None:
            key = cls._generate_registry_key(provider_name, None, async_client=async_client)
        else:
            if astral_client.new_client:
                if astral_client.client_key:
                    key = cls._generate_registry_key(provider_name, None, astral_client.client_key, async_client)
                else:
                    raise ValueError(
                        "When new_client is True, you must provide a unique client_key."
                    )
            else:
                key = cls._generate_registry_key(
                    provider_name, 
                    astral_client.client_config, 
                    astral_client.client_key,
                    async_client
                )

        with cls._lock:
            if key not in cls._client_registry:
                client_class = _PROVIDER_CLIENT_MAP.get(provider_name)
                if client_class is None:
                    raise ProviderNotSupportedError(provider_name=provider_name)
                cls._client_registry[key] = client_class(
                    astral_client.client_config if astral_client else None,
                    async_client=async_client
                )
            return cls._client_registry[key]

    @classmethod
    def register_client(
        cls,
        provider_name: ModelProvider,
        client: BaseProviderClient,
        client_config: Optional[AUTH_CONFIG_TYPE] = None,
        client_key: Optional[str] = None,
        async_client: bool = False,
    ) -> None:
        """
        Manually register or replace a provider client.
        
        Args:
            provider_name: The name of the provider
            client: The client instance to register
            client_config: Optional configuration for the client
            client_key: Optional unique key for the client
            async_client: Whether this is an async client (default: False)
        """
        key = cls._generate_registry_key(provider_name, client_config, client_key, async_client)
        with cls._lock:
            cls._client_registry[key] = client

    @classmethod
    def unregister_client(
        cls,
        provider_name: ModelProvider,
        client_config: Optional[AUTH_CONFIG_TYPE] = None,
        client_key: Optional[str] = None,
        async_client: bool = False,
    ) -> None:
        """
        Unregister a provider client.
        
        Args:
            provider_name: The name of the provider
            client_config: Optional configuration for the client
            client_key: Optional unique key for the client
            async_client: Whether this is an async client (default: False)
        """
        key = cls._generate_registry_key(provider_name, client_config, client_key, async_client)
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
