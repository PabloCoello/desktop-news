from openai import OpenAI
from openai import AsyncOpenAI
import json
from desktop_news.nytAPI import NYTimesTopStoriesAPI
from base64 import b64decode
from datetime import datetime
import subprocess
import os
from typing import Awaitable
import asyncio
import sys

WD = os.path.expandvars("${HOME}/.config/desktop-news")


def get_news(nyt):
    # Obtener noticias
    abstracts = nyt.get_top_abstracts()
    # Generar texto adicional basado en los titulares
    texto_generado = ""
    for idx, abstract in enumerate(abstracts, start=1):
        texto_generado += f"Noticia: {abstract}\n"
    return texto_generado


def convert_image(filename):
    with open(f"{WD}/responses/{filename}", mode="r", encoding="utf-8") as file:
        response = json.load(file)
    image_data = b64decode(response)
    image_file = f"{WD}/images/{filename}.png"
    with open(image_file, mode="wb") as png:
        png.write(image_data)


def save_image(filename, response):
    with open(f"{WD}/responses/{filename}", mode="w", encoding="utf-8") as file:
        json.dump(response.data[0].b64_json, file)


def generate_image(client, prompt, set_wallpaper=False):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size='1792x1024',
        quality="standard",
        n=1,
        response_format="b64_json"
    )
    filename = f"{datetime.today().date().isoformat()}-{response.created}"
    save_image(filename, response)
    convert_image(filename)
    if set_wallpaper:
        # Comando para cambiar el fondo de pantalla
        comando = f"gsettings set org.gnome.desktop.background picture-uri-dark file://{f'{WD}/images/{filename}.png'}"
        # Ejecutar el comando
        subprocess.run(comando, shell=True)


async def get_prompt(provider, prompts, news) -> Awaitable[str]:
    completion = await provider.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompts.get("summary") + news}])
    return completion

def main():
    with open(f"{WD}/conf.json", "r") as f:
        conf = json.load(f)
        client = OpenAI(api_key=conf.get("openai_api_key"))
        asyn = AsyncOpenAI(api_key=conf.get("openai_api_key"))
        nyt = NYTimesTopStoriesAPI(conf.get('nyt_api_key'))

    with open(f"{WD}/prompt.json") as f:
        prompts = json.load(f)

    news = get_news(nyt)
    completion = asyncio.run(get_prompt(asyn, prompts, news))
    prompt = completion.dict()['choices'][0]['message']["content"]
    prompt = prompt + \
        f" Create the image like everything is happening in the following environment/universe/scenario: {sys.argv[1]}." if len(
            sys.argv) > 1 else prompt
    print(prompt)
    generate_image(client, prompt, set_wallpaper=True)

if __name__ == "__main__":
    main()
