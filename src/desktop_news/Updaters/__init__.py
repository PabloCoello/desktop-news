import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("desktop_news." + os.path.dirname(__file__).split("/")
               [-1] + "." + module[:-3], locals(), globals())
del module
