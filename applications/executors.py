from piper.base.executors import FastAPIExecutor

from pydantic import BaseModel


class StringValue(BaseModel):
    value: str


class TestMessageAdder(FastAPIExecutor):

    def __init__(self, appender="TEST", **kwargs):
        self.appender = appender
        super().__init__(**kwargs)

    def scripts(self):
        return [__file__]

    async def run(self, message: StringValue) -> StringValue:
        return StringValue(value=(message.value + self.appender))
