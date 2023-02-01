from piper.base.executors.fastapi import FastAPIExecutor


class Agent(FastAPIExecutor):
    """
    Run pipelines using http requests.
    Send your pipeline as json to agent to run Piper pipeline.
    You can use agent to organize your no-code UI similar to our.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def run(self, pipeline: dict) -> dict:
        pass