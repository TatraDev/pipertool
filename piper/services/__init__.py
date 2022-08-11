from pydantic import BaseModel

from piper.base.executors import FastAPIExecutor, VirtualEnvExecutor


class StringValue(BaseModel):
    value: str


class TestMessageAdder(FastAPIExecutor):

    def __init__(self, appender="TEST", **kwargs):
        self.appender = appender
        super().__init__(**kwargs)

    async def run(self, message: StringValue) -> StringValue:
        return StringValue(value=(message.value + self.appender))

