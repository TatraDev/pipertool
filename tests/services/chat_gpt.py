import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
loop = asyncio.get_event_loop()

from piper.services.chat_gpt import ChatGPT, StringValue
from piper.envs import DockerEnv, CurrentEnv, VirtualEnv


class TestPiperBase:

    def test_chat_gpt(self):
        session_token = os.getenv("CHAT_GPT_SESSION_TOKEN")
        service = ChatGPT(session_token)
        prompt_s = "what is 2 + 2 ?"
        x = StringValue(value=prompt_s)

        with CurrentEnv() as env:
            result = service(x)
            print(result)
            assert "4" in result["message"]


