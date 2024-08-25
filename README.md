# desktop-news

The objective of this repository is to generate an image with DALL-E from a prompt generated with chatgpt4 from the abstracts of the main world news obtained from the New York Times API.

In addition, it is possible to set the image in some scenario/universe/environment by executing the script passing an argument with the name of the desired environment (“star wars”, “Mad Max”, “Marvel”...).

In order to execute correctly the main.py script it is necessary to introduce first the api keys of openai and the api of New York Times in the file ~/config/conf.json.

# installation

Build and install using build and pip.

```bash
# install build package
pip install build

# build desktop-news
python3 -m build

# install generated whl package
pip install dist/version.whl
```

If you are working in development and you are not changing pyproject.toml version do not forget to force reinstall:

```bash
# install generated whl package
pip install dist/version.whl --force-reinstall
```

Once installed generate conf file using `--generateconf` arg:

```bash
desktop-news --generateconf
```

This will generate `~/.config/desktop-news/conf.json` conf file, remember to update it with your api tokens.

# usage

Run desktop-news --help

```txt
usage: desktop-news [-h] [-c CONFIG] [-s SCENARIO] [--generateconf] [--silent]

tool that generates wallpaper using AI from multiple sources of daily news

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        configuration file
  -s SCENARIO, --scenario SCENARIO
                        base scenario of generation
  --generateconf        generate configuration file template
  --silent              silent output
```

Once conf file is updated with your tokens and desired paths you can execute desktop-news:

```bash
desktop-news
```

This will query NYT api to get todays news and generate an image using DALL-E and store it on your configures images path.

If you want to personalise the style of the image you can use --scenario option:

```bash
desktop-news -s star-wars
```

If you have different configuration files you can indicate conf file with --config option:

```bash
desktop-news -c ./path/to/another/conf
```

By default mean while it works shows an animation, if you want to get rig of that use `--silent` option:

```bash
desktop-news --silent
```

desktop-news once finish will output the path to the generated image, so you can pipe it to your set up wallpaper command.

# example wallpaper set up

```bash
gsettings set org.gnome.desktop.background picture-uri-dark file://"$(desktop-news --silent -s marvel)"
```


