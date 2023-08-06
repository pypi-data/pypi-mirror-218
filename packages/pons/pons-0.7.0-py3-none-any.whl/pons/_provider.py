from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Any, AsyncIterator, Dict, Optional, Union, cast, Iterable, Mapping, Tuple

import httpx


# TODO: the doc entry had to be written manually for this type because of Sphinx limitations.
JSON = Union[bool, int, float, str, None, Iterable["JSON"], Mapping[str, "JSON"]]


class Provider(ABC):
    """
    The base class for JSON RPC providers.
    """

    @abstractmethod
    @asynccontextmanager
    async def session(self) -> AsyncIterator["ProviderSession"]:
        """
        Opens a session to the provider
        (allowing the backend to perform multiple operations faster).
        """
        yield  # type: ignore


class UnexpectedResponse(Exception):
    """
    Raised when the remote server's response is not of an expected format.
    """


class ResponseDict:
    """
    A wrapper for dictionaries allowing as to narrow down KeyErrors
    resulting from an incorrectly formatted response.
    """

    def __init__(self, response: Any):
        if not isinstance(response, dict):
            raise UnexpectedResponse(
                f"Expected a dictionary as a response, got {type(response).__name__}"
            )
        if not all(isinstance(key, str) for key in response):
            raise UnexpectedResponse(f"Some keys in the response are not strings: {response}")
        self._response = cast(Dict[str, JSON], response)

    def __contains__(self, field: str) -> bool:
        return field in self._response

    def __getitem__(self, field: str) -> JSON:
        try:
            contents = self._response[field]
        except KeyError as exc:
            raise UnexpectedResponse(
                f"Expected field `{field}` is missing from the result"
            ) from exc
        return contents


class ProviderSession(ABC):
    """
    The base class for provider sessions.
    """

    @abstractmethod
    async def rpc(self, method: str, *args: JSON) -> JSON:
        """
        Calls the given RPC method with the already json-ified arguments.
        """
        ...

    async def rpc_and_pin(self, method: str, *args: JSON) -> Tuple[JSON, Tuple[int, ...]]:
        """
        Calls the given RPC method and returns the path to the provider it succeded on.
        This method will be typically overriden by multi-provider implementations.
        """
        return await self.rpc(method, *args), ()

    async def rpc_at_pin(self, path: Tuple[int, ...], method: str, *args: JSON) -> JSON:
        """
        Calls the given RPC method at the provider by the given path
        (obtained previously from ``rpc_and_pin()``).
        This method will be typically overriden by multi-provider implementations.
        """
        if path != ():
            raise ValueError(f"Unexpected provider path: {path}")
        return await self.rpc(method, *args)

    async def rpc_dict(self, method: str, *args: JSON) -> Optional[ResponseDict]:
        """
        Calls the given RPC method expecting to get a dictionary (or ``null``) in response.
        """
        result = await self.rpc(method, *args)
        if result is None:
            return None
        return ResponseDict(result)


class HTTPProvider(Provider):
    """
    A provider for RPC via HTTP(S).
    """

    def __init__(self, url: str):
        self._url = url

    @asynccontextmanager
    async def session(self) -> AsyncIterator["HTTPSession"]:
        async with httpx.AsyncClient() as client:
            yield HTTPSession(self._url, client)


class RPCError(Exception):
    """
    A wrapper for a server error returned either as a proper RPC response,
    or as an HTTP error code response.
    """

    @classmethod
    def from_json(cls, response: JSON) -> "RPCError":
        error = ResponseDict(response)
        if "data" in error:
            data = error["data"]
            if data is not None and not isinstance(data, str):
                raise UnexpectedResponse(
                    f"Error data must be a string or None, got {type(data)} ({data})"
                )
        else:
            data = None

        error_code = error["code"]
        if isinstance(error_code, str):
            code = int(error_code)
        elif isinstance(error_code, int):
            code = error_code
        else:
            raise UnexpectedResponse(
                "Error code must be an integer (possibly string-encoded), "
                f"got {type(error_code)} ({error_code})"
            )

        message = error["message"]
        if not isinstance(message, str):
            raise UnexpectedResponse(
                f"Error message must be a string, got {type(message)} ({message})"
            )

        return cls(code, message, data)

    def __init__(self, code: int, message: str, data: Optional[str] = None):
        super().__init__(code, message, data)
        self.code = code
        self.message = message
        self.data = data


class Unreachable(Exception):
    """
    Raised when there is a problem connecting to the provider.
    """


class HTTPSession(ProviderSession):
    def __init__(self, url: str, http_client: httpx.AsyncClient):
        self._url = url
        self._client = http_client

    async def rpc(self, method: str, *args: JSON) -> JSON:
        json = {"jsonrpc": "2.0", "method": method, "params": args, "id": 0}
        try:
            response = await self._client.post(self._url, json=json)
        except Exception as exc:
            raise Unreachable(str(exc)) from exc
        if response.status_code != HTTPStatus.OK:
            raise RPCError(response.status_code, response.content.decode())

        response_json = response.json()
        if not isinstance(response_json, Mapping):
            raise UnexpectedResponse(f"RPC response must be a dictionary, got: {response_json}")
        # Assuming that the HTTP client knows what it's doing, and gives us a valid JSON dict
        response_json = cast(Mapping[str, JSON], response_json)
        if "error" in response_json:
            raise RPCError.from_json(response_json["error"])
        if "result" not in response_json:
            raise UnexpectedResponse(f"`result` is not present in the response: {response_json}")
        return response_json["result"]
