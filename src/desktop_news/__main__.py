import os
import sys
import json
import argparse
import subprocess
import logging

from base64 import b64decode
from datetime import datetime
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

args = parser.parse_args()


def save_image(conf, response):
    # b = json.loads(response["b64"])
    image_data = b64decode(response["b64"])
    filename = f"{datetime.today().date().isoformat()}-{response['created']}.png"
    image_file = f"{conf['image_path']}/{filename}"
    with open(image_file, mode="+wb") as png:
        png.write(image_data)
        print(image_file)


def main():
    if args.generateconf:
        generate_conf_file_template("/".join(args.config.split("/")[:-1]))
        sys.exit(0)
    try:
        with open(args.config, "r") as f:
            conf = json.load(f)
            prompts = conf.get("prompt")
    except FileNotFoundError:
        print("conf file not found, launch with --generate-conf to auto generate it on ~/.config/desktop-news/")
        sys.exit(1)

    builder = PromptBuilder(conf, args)
    preprocess = OpenAIPreprocessor(conf, args)
    generator = OpenAIGenerator(conf, args)

    prompt_content = builder.build_prompt(exclude_tags=["literal"])
    prompt = preprocess.preprocess(prompt_content)
    prompt += builder.build_prompt(include_tags=["literal"])
    res = generator.generate(prompt)
    save_image(conf, res)


if __name__ == "__main__":
    main()
