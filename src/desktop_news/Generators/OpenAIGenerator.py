import asyncio
from typing import Awaitable

from desktop_news.IGenerator import IGenerator

from openai import OpenAI


class OpenAIGenerator(IGenerator):
    def __init__(self, conf, args):
        self.conf_ = conf["image"]
        self.openai_ = OpenAI(api_key=conf.get("openai_api_key"))

    def generate(self, prompt) -> dict:
        conf = self.conf_
        conf.update(dict(prompt=prompt, n=1, response_format="b64_json"))
        response = self.openai_.images.generate(**conf)
        return dict(created=response.created, b64=response.data[0].b64_json)
