import time

from fastapi import FastAPI, Request
from piper.base.executors import LocalEnvironment

from executors import TestMessageAdder, StringValue, StringValue

app = FastAPI()

with LocalEnvironment():
    executor = TestMessageAdder(  )

    @app.post('/run')
    async def run(
        request_model: StringValue,
    ):
        result = await executor.run(request_model)

        return result.dict()