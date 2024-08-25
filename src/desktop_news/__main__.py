import os
import sys
import json
import argparse
import asyncio
import subprocess
import logging

from desktop_news.nytAPI import NYTimesTopStoriesAPI
from base64 import b64decode
from datetime import datetime
from typing import Awaitable
from desktop_news.ConfFileManager import generate_conf_file_template

from openai import OpenAI
from openai import AsyncOpenAI


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


def get_news(nyt):
    # Obtener noticias
    abstracts = nyt.get_top_abstracts()
    # Generar texto adicional basado en los titulares
    texto_generado = ""
    for idx, abstract in enumerate(abstracts, start=1):
        texto_generado += f"Noticia: {abstract}\n"
    return texto_generado


def convert_image(image_path, response_path, filename):
    with open(f"{response_path}/{filename}", mode="r", encoding="utf-8") as file:
        response = json.load(file)
    image_data = b64decode(response)
    image_file = f"{image_path}/{filename}.png"
    with open(image_file, mode="wb") as png:
        png.write(image_data)


def save_image(response_path, filename, response):
    with open(f"{response_path}/{filename}", mode="w", encoding="utf-8") as file:
        json.dump(response.data[0].b64_json, file)


def generate_image(conf, client, prompt, set_wallpaper=False):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size='1792x1024',
        quality="standard",
        n=1,
        response_format="b64_json"
    )
    filename = f"{datetime.today().date().isoformat()}-{response.created}"
    save_image(conf["response_path"],  filename, response)
    convert_image(conf["image_path"], conf["response_path"], filename)
    if set_wallpaper:
        # Command to change wallpaper
        # TODO(dcoello): remove this or change sink actions to generic.
        path = conf["image_path"]
        command = f"gsettings set org.gnome.desktop.background picture-uri-dark file://{f'{path}/{filename}.png'}"
        subprocess.run(command, shell=True)


async def get_prompt(provider, prompts, news) -> Awaitable[str]:
    completion = await provider.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompts.get("summary") + news}])
    return completion


def main():

    if args.generateconf:
        generate_conf_file_template("/".join(args.config.split("/")[:-1]))
        sys.exit(0)

    try:
        with open(args.config, "r") as f:
            conf = json.load(f)
            client = OpenAI(api_key=conf.get("openai_api_key"))
            asyn = AsyncOpenAI(api_key=conf.get("openai_api_key"))
            nyt = NYTimesTopStoriesAPI(conf.get('nyt_api_key'))
            prompts = conf.get("prompt")
    except FileNotFoundError:
        print("conf file not found, launch with --generate-conf to auto generate it on ~/.config/desktop-news/")
        sys.exit(1)

    news = get_news(nyt)
    completion = asyncio.run(get_prompt(asyn, prompts, news))
    prompt = completion.dict()['choices'][0]['message']["content"]
    prompt = prompt + \
        f" Create the image like everything is happening in the following environment/universe/scenario: {args.scenario}."
    print(prompt)
    generate_image(conf, client, prompt, set_wallpaper=True)


if __name__ == "__main__":
    main()
