from abc import abstractmethod

import aiohttp

from piper.envs import get_env, is_current_env
from piper.utils.logger_utils import logger
from piper.base.executors import BaseExecutor
from pydantic import BaseModel


def is_known(obj):
    basic = obj.__class__.__name__ in {'dict', 'list', 'tuple', 'str', 'int', 'float', 'bool'}
    models = isinstance(obj, (BaseModel,))
    return basic or models


def prepare(obj):
    if isinstance(obj, (BaseModel,)):
        return obj.dict()
    return obj


def inputs_to_dict(*args, **kwargs):
    from_args = {}
    for arg in args:
        if is_known(arg):
            from_args.update(prepare(arg))
    from_kwargs = {k: prepare(v) for k, v in kwargs.items() if is_known(v)}
    from_args.update(from_kwargs)
    return from_args


class HTTPExecutor(BaseExecutor):

    def __init__(self, host: str, port: int, base_handler: str):
        self.host = host
        self.port = port
        self.base_handler = base_handler

    @abstractmethod
    async def run(self, *args, **kwargs):
        pass

    async def __call__(self, *args, **kwargs):
        logger.info(f'call in env {get_env()}')

        if is_current_env():
            return await self.run(*args, **kwargs)
        else:
            function = self.base_handler
            request_dict = inputs_to_dict(*args, **kwargs)
            logger.info(f'request_dict is {request_dict}')
            async with aiohttp.ClientSession() as session:
                url = f'http://{self.host}:{self.port}/{function}'
                logger.info(f'run function with url {url} and data {request_dict}')
                async with session.post(url, json=request_dict) as resp:
                    return await resp.json()
