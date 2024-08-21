# desktop-news

El objetivo de este repositorio es generar una imagen con DALL-E a partir de un prompt generado con chatgpt4 a partir de los abstracts de las principales noticias mundiales obtenidos a partir del API del New York Times.

Además, esposible ambientar la imagen en algún escenario/universo/entorno mediante la ejecución del script pasando un argumento con el nombre del entorno que se desee ("star wars", "Mad max", "Marvel"...).

Para poder ejecutar correctamente el script main.py es necesario introducir primero las api keys de openai y del api de New York Times en el fichero ./conf/conf.json.

## Automatizar wallpaper diario en Ubuntu

Si además se desea automatizar el cambio de wallpaper de forma diaria en Ubuntu a partir de la imagen generada por este repo es necesario seguir los siguientes pasos:

-   Utiliza cron para programar la ejecución periódica de main.py. Puedes abrir el cron job configurando la tabla de cron con el comando: "crontab -e" y programar la ejecución introduciendo la siguiente línea de código "0 8 * * * /ruta/a/tu/script.py".

-   Dar los permisos adecuados al script main.py con "chmod +x /ruta/a/tu/script.py"