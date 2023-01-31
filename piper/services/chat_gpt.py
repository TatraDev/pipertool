from piper.imports import safe_import
from piper.base.executors.fastapi import FastAPIExecutor
from piper.services import StringValue
from piper.utils.logger_utils import logger

with safe_import():
    from revChatGPT.ChatGPT import Chatbot


class ChatGPT(FastAPIExecutor):

    requirements = FastAPIExecutor.requirements + ["revChatGPT"]

    def __init__(self, session_token: str):
        """
        Add CHAT_GPT_SESSION_TOKEN to your .env file please
        Look here for the instructions
        https://github.com/acheong08/ChatGPT/wiki/Setup
        """
        self.chatbot = Chatbot({
            "session_token": session_token
        }, conversation_id=None, parent_id=None)
        super().__init__()

    async def run(self, prompt: StringValue):
        self.chatbot.reset_chat()
        response = self.chatbot.ask(prompt.value, conversation_id=None, parent_id=None)
        logger.info(f"chatGPT response for {prompt.value} is {response}")

        return response
