import os
import sys
import json
import logging

CONF_FILE_TEMPLATE=dict(
    nyt_api_key="your nyt api key",
    openai_api_key="yout openai api key",
    prompt=dict(
        summary="below you will find a series of relevant news of today. could you summarize them and try to combine them into a single text with no more than 4 sentences?, i would also like you make all the necessary modifications to comply with dall-e's usage policies (avoid mention ethnicities, race, violent language and anything that could offend anyone):"
    ),
    response_path="/tmp/",
    image_path="~/images"
)

def generate_conf_file_template(path:str):
    if not os.path.exists(path):
        os.makedirs(path)

    conf_file_path = f"{path}/conf.json"
    with open(conf_file_path, "+w") as file:
        content = json.dumps(CONF_FILE_TEMPLATE, indent=2)
        file.write(content)
        logging.debug(conf_file_path)
        logging.debug(content)

