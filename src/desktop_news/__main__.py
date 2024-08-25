import os
import sys
import json
import argparse
import subprocess
import logging

from base64 import b64decode
from datetime import datetime
from rich.console import Console
from desktop_news.ConfFileManager import generate_conf_file_template
from desktop_news.PromptBuilder import PromptBuilder
from desktop_news.Preprocessors.OpenAIPreprocessor import OpenAIPreprocessor
from desktop_news.Generators.OpenAIGenerator import OpenAIGenerator


parser = argparse.ArgumentParser(
    description="tool that generates wallpaper using AI from multiple sources of daily news")

parser.add_argument(
    '-c', '--config',
    default=os.path.expanduser('~') + "/.config/desktop-news/conf.json",
    help="configuration file")

parser.add_argument(
    '-s', '--scenario',
    default="daily news",
    help="base scenario of generation")

parser.add_argument(
    '--generateconf',
    action="store_true",
    help="generate configuration file template")

parser.add_argument(
    '--silent',
    action="store_true",
    help="silent output")

args = parser.parse_args()


def save_image(conf, response):
    image_data = b64decode(response["b64"])
    filename = f"{datetime.today().date().isoformat()}-{response['created']}.png"
    image_file = os.path.expanduser(f"{conf['image_path']}/{filename}")
    with open(image_file, mode="+wb") as png:
        png.write(image_data)
        print(image_file)


class FakeContext:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass


class FakeConsole:
    def __init__(self):
        pass

    def status(self, msg):
        return FakeContext()

    def log(self, msg):
        pass


def main():
    console = FakeConsole() if args.silent else Console()
    if args.generateconf:
        generate_conf_file_template("/".join(args.config.split("/")[:-1]))
        sys.exit(0)
    try:
        with open(args.config, "r") as f:
            conf = json.load(f)
            prompts = conf.get("prompt")
    except FileNotFoundError:
        console.log(
            "conf file not found, launch with --generate-conf to auto generate it on ~/.config/desktop-news/")
        sys.exit(1)

    with console.status("[bold green]Generating...") as status:
        builder = PromptBuilder(conf, args)
        preprocess = OpenAIPreprocessor(conf, args)
        generator = OpenAIGenerator(conf, args)

        console.log("building prompt")
        prompt_content = builder.build_prompt(exclude_tags=["literal"])
        console.log("preprocess prompt")
        prompt = preprocess.preprocess(prompt_content)
        prompt += builder.build_prompt(include_tags=["literal"])
        console.log("generate image")
        res = generator.generate(prompt)
        console.log("save image")
        save_image(conf, res)


if __name__ == "__main__":
    main()
