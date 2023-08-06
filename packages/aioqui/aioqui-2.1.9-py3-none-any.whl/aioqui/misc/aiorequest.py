from aiohttp import ClientSession
from contextlib import suppress
from functools import lru_cache, wraps
from ast import literal_eval
from typing import Any
from uuid import UUID
import ujson


unset = ['unser']


class CachedAwaitable:
    def __init__(self, awaitable):
        self.awaitable = awaitable
        self.result = unset

    def __await__(self):
        if self.result is unset:
            self.result = yield from self.awaitable.__await__()
        return self.result


def reawaitable(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return CachedAwaitable(func(*args, **kwargs))
    return wrapper


def aiocache(maxsize=128, typed=False):
    if callable(maxsize) and isinstance(typed, bool):
        user_function, maxsize = maxsize, 128
        return lru_cache(maxsize, typed)(reawaitable(user_function))

    def decorating_function(user_function):
        return lru_cache(maxsize, typed)(reawaitable(user_function))

    return decorating_function


class Request:
    baseurl: str

    async def __call__(
            self,
            method: str, url: str,
            *,
            params: dict[str, Any] = None,
            headers: dict[str, Any] = None,
            body: dict[str, Any] = None,
            data: dict[str, Any] = None,
            deserialize: bool = False
    ) -> Any:
        if params:  # convert params values to str
            params = {key: str(value) for key, value in params.items()}
        if (method := method.lower()) not in ('get', 'post', 'put', 'delete'):
            raise NotImplementedError(f'method: {method} is not supported by `aiorequest.request`')
        async with ClientSession(json_serialize=ujson.dumps) as session:
            async with getattr(session, method)(
                    await self.__url(url),
                    json=await self.serialize(body), params=params, headers=headers, data=data
            ) as response:
                try:
                    json = await response.json()
                    if deserialize:
                        json = await self.deserialize(json)
                    return json
                except Exception as error:
                    return error

    async def get(self, url: str, **kwargs) -> Any:
        return await self('get', url, **kwargs)

    async def post(self, url: str, **kwargs) -> Any:
        return await self('post', url, **kwargs)

    async def put(self, url: str, **kwargs) -> Any:
        return await self('put', url, **kwargs)

    async def delete(self, url: str, **kwargs) -> Any:
        return await self('delete', url, **kwargs)

    # @aiocache
    async def __url(self, url: str):
        if not (base := self.baseurl) or url.startswith('http'):
            return url
        if base.endswith('/') and url.startswith('/'):
            return base[:-1] + url
        if base.endswith('/') and not url.startswith('/'):
            return base + url
        if not base.endswith('/') and url.startswith('/'):
            return base + url
        # if not base.endswith('/') and not url.startswith('/'):
        return f'{base}/{url}'

    @staticmethod
    # @aiocache
    async def serialize(data: Any) -> Any:
        if isinstance(data, dict):
            return {key: await Request.serialize(value) for key, value in data.items()}
        if isinstance(data, list):
            return [await Request.serialize(element) for element in data]
        if isinstance(data, (int, float, bool, str)) or data is None:
            return data
        return str(data)

    @staticmethod
    # @aiocache
    async def deserialize(json: Any) -> Any:
        # handles dict
        if isinstance(json, dict):
            return {key: await Request.deserialize(value) for key, value in json.items()}
        # handles list
        if isinstance(json, list):
            return [await Request.deserialize(element) for element in json]
        # converts the value
        from dateutil import parser  # imported in the function, since package is not built-in

        # 'ed38fe7a-11e6-4c59-ac31-ef30848e8e83' to UUID('ed38fe7a-11e6-4c59-ac31-ef30848e8e83')
        with suppress(Exception):
            return UUID(json)
        # '2023-06-09 21:52:49.072155' to datetime.datetime(2023, 6, 9, 21, 52, 49, 72155)
        with suppress(Exception):
            return parser.parse(json)
        # (1, 1.1, True) remains as it is
        if isinstance(json, (int, float, bool)):
            return json
        # "b'bytes'" to b'bytes'
        with suppress(Exception):
            return literal_eval(json)
        # 'string' remains as it is
        if isinstance(json, str):
            return json
        # 'null' to None
        return None


request = Request()
