from openai import OpenAI
from openai import AsyncOpenAI
import json
from nytAPI import NYTimesTopStoriesAPI
from base64 import b64decode
from datetime import datetime
import subprocess
import os

def get_news():
    # Obtener noticias
    abstracts = nyt.get_top_abstracts()
    # Generar texto adicional basado en los titulares
    texto_generado = ""
    for idx, abstract in enumerate(abstracts, start=1):
        texto_generado += f"Noticia: {abstract}\n"
    return texto_generado

def convert_image(filename):
    with open(f"./responses/{filename}", mode="r", encoding="utf-8") as file:
        response = json.load(file)
    image_data = b64decode(response)
    image_file = f"./images/{filename}.png"
    with open(image_file, mode="wb") as png:
        png.write(image_data)

def save_image(filename, response):
    with open(f"./responses/{filename}", mode="w", encoding="utf-8") as file:
        json.dump(response.data[0].b64_json, file)

def generate_image(prompt, set_wallpaper=False):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size='1792x1024',
        quality="standard",
        n=1,
        response_format="b64_json"
    )
    filename=f"{datetime.today().date().isoformat()}-{response.created}"
    save_image(filename, response)
    convert_image(filename)
    if set_wallpaper:
        # Comando para cambiar el fondo de pantalla
        comando = f"gsettings set org.gnome.desktop.background picture-uri file://{f'{os.getcwd()}/images/{filename}.png'}"
        # Ejecutar el comando
        subprocess.run(comando, shell=True)

if __name__ == "__main__":
    
    with open("./conf/conf.json") as f:
        conf = json.load(f)
        client = OpenAI(api_key=conf.get("openai_api_key"))
        asyn = AsyncOpenAI(api_key=conf.get("openai_api_key"))
        nyt = NYTimesTopStoriesAPI(conf.get('nyt_api_key'))

    with open("./conf/prompt.json") as f:
        prompts = json.load(f)

    news = get_news()
    completion = await asyn.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompts.get("summary") +news}])
    prompt = completion.dict()['choices'][0]['message']["content"]
    generate_image(prompt, set_wallpaper=True)
