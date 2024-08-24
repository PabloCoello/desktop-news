import asyncio
from typing import Awaitable

from desktop_news.IPreprocessor import IPreprocessor

from openai import AsyncOpenAI


class OpenAIPreprocessor(IPreprocessor):
    def __init__(self, conf, args):
        self.openai_ = AsyncOpenAI(api_key=conf.get("openai_api_key"))

    def preprocess(self, prompt) -> str:
        completion = asyncio.run(self.get_prompt(prompt))
        return completion.dict()['choices'][0]['message']["content"]

    async def get_prompt(self, prompt) -> Awaitable[str]:
        completion = await self.openai_.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content":  prompt}])
        return completion
