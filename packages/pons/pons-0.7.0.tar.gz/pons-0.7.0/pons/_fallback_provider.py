from abc import ABC, abstractmethod
from contextlib import asynccontextmanager, AsyncExitStack
from typing import Any, AsyncIterator, Optional, Iterable, List, Tuple, Union

from ._provider import Provider, ProviderSession, JSON, RPCError, UnexpectedResponse


class FallbackStrategy(ABC):
    """
    An abstract class defining a fallback strategy for multiple providers.
    """

    @abstractmethod
    def get_provider_order(self) -> List[int]:
        """
        Returns the suggested order of providers to query, based on the accumulated data.
        This method is called once on every high-level request to the provider.
        """


class FallbackStrategyFactory(ABC):
    """
    An abstract class defining a fallback strategy factory for multiple providers.
    This will be called in ``FallbackProvider`` to create an actual strategy object
    (which may be mutated).
    """

    @abstractmethod
    def make_strategy(self, num_providers: int) -> FallbackStrategy:
        """
        Returns a strategy object.
        """


class CycleFallbackStrategy(FallbackStrategy):
    def __init__(self, weights: List[int]):
        self._providers = list(range(len(weights)))
        self._weights = weights
        self._counter = 0

    def get_provider_order(self) -> List[int]:
        if self._counter == self._weights[0]:
            self._counter = 0
            self._providers = self._providers[1:] + [self._providers[0]]
            self._weights = self._weights[1:] + [self._weights[0]]

        self._counter += 1
        return list(self._providers)


class CycleFallback(FallbackStrategyFactory):
    """
    Creates a strategy where the providers are cycled such that the number of times
    a given provider is first in the priority list is equal
    to the corresponding entry in ``weights``
    (the length of which should match the number of providers).
    If ``weights`` is not given, a list of ``1`` will be used.
    """

    def __init__(self, weights: Optional[Iterable[int]] = None):
        self._weights: Optional[List[int]]
        if weights:
            self._weights = list(weights)
        else:
            self._weights = None

    def make_strategy(self, num_providers: int) -> CycleFallbackStrategy:
        if not self._weights:
            weights = [1] * num_providers
        else:
            weights = self._weights

        if len(weights) != num_providers:
            raise ValueError(
                f"Length of the weights ({len(weights)}) "
                f"inconsistent with the number of providers ({num_providers})"
            )

        return CycleFallbackStrategy(weights)


class PriorityFallbackStrategy(FallbackStrategy):
    """
    Creates a strategy where the providers are queried in the order
    they were given to ``FallbackProvider``, until a successful response is received.
    """

    def __init__(self, num_providers: int):
        self._providers = list(range(num_providers))

    def get_provider_order(self) -> List[int]:
        return self._providers


class PriorityFallback(FallbackStrategyFactory):
    def make_strategy(self, num_providers: int) -> PriorityFallbackStrategy:
        return PriorityFallbackStrategy(num_providers)


class FallbackProvider(Provider):
    """
    A provider that encompasses several providers and for every request
    tries every one of them until the request is successful.
    The order is chosen according to the given strategy.

    If ``same_provider`` is ``True``, the given providers are treated as endpoints
    pointing to the same physical provider, for the purpose of stateful requests
    (e.g. filter creation).

    If all requests finished with an error, the most informative error is raised.
    """

    def __init__(
        self,
        providers: Iterable[Provider],
        strategy: FallbackStrategyFactory = PriorityFallback(),
        same_provider: bool = False,
    ):
        self._providers = list(providers)
        self._strategy = strategy.make_strategy(len(self._providers))
        self._same_provider = same_provider

    @asynccontextmanager
    async def session(self) -> AsyncIterator["ProviderSession"]:
        async with AsyncExitStack() as stack:
            sessions = []
            for provider in self._providers:
                sessions.append(await stack.enter_async_context(provider.session()))
            yield FallbackProviderSession(sessions, self._strategy, self._same_provider)


class FallbackProviderSession(ProviderSession):
    def __init__(
        self, sessions: List[ProviderSession], strategy: FallbackStrategy, same_provider: bool
    ):
        self._sessions = sessions
        self._strategy = strategy
        self._same_provider = same_provider

    async def rpc_and_pin(self, method: str, *args: JSON) -> Tuple[JSON, Tuple[int, ...]]:
        exceptions: List[Exception] = []
        provider_idxs = self._strategy.get_provider_order()
        for provider_idx in provider_idxs:
            try:
                result, sub_idx = await self._sessions[provider_idx].rpc_and_pin(method, *args)
            except Exception as exc:
                exceptions.append(exc)
            else:
                return result, (provider_idx,) + sub_idx

        # Here we may have a list with each element being
        # `RPCError`, `UnexpectedResponse`, or `Unreachable`.
        # Since the users of `Provider` rely on the error being one of these types,
        # we can only raise one. So we raise the one with the most information.
        rpc_errors = [exc for exc in exceptions if isinstance(exc, RPCError)]
        if len(rpc_errors) > 0:
            raise rpc_errors[0]
        unexpecteds = [exc for exc in exceptions if isinstance(exc, UnexpectedResponse)]
        if len(unexpecteds) > 0:
            raise unexpecteds[0]
        raise exceptions[0]

    async def rpc(self, method: str, *args: JSON) -> JSON:
        result, _provider = await self.rpc_and_pin(method, *args)
        return result

    async def rpc_at_pin(self, path: Tuple[int, ...], method: str, *args: JSON) -> JSON:
        if self._same_provider:
            return await self.rpc(method, *args)
        if not path or path[0] < 0 or path[0] >= len(self._sessions):
            raise ValueError(f"Invalid provider path: {path}")
        return await self._sessions[path[0]].rpc_at_pin(path[1:], method, *args)
