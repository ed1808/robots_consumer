import json
import requests

from pathlib import Path
from time import sleep
from sys import exit
from simple_colors import *

from http_status_codes import CLIENT_ERRORS_DICT, SERVER_ERRORS_DICT

robot_config = {}
json_error = False
error_detail = ''

try:
    with open(Path.cwd() / 'robots.json') as f:
        try:
            robot_config = json.loads(f.read())
        except json.JSONDecodeError:
            json_error = True
            print(
                f'{red("[CONSUMER MESSAGE]:", "bold")} El JSON está mal estructurado, por favor revísalo')
        finally:
            f.close()
except FileNotFoundError:
    print(
        f'{red("[CONSUMER MESSAGE]:", "bold")} El archivo {yellow("robots.json", ["bold", "italic"])} no existe en el directorio actual')
    print(f'{red("[CONSUMER MESSAGE]:", "bold")} El path actual es: {Path.cwd()}')
    
    exit(-1)

if json_error:
    exit(-1)

try:
    while True:

        for url in robot_config['robotsUrls']:
            print(f'{green("[CONSUMER MESSAGE]:", "bold")} Consultando {url}')

            try:
                response = requests.get(url)

                if response.status_code in CLIENT_ERRORS_DICT or response.status_code in SERVER_ERRORS_DICT:
                    if response.status_code in CLIENT_ERRORS_DICT:
                        error_detail = CLIENT_ERRORS_DICT[response.status_code].get(
                            'message')
                    else:
                        error_detail = SERVER_ERRORS_DICT[response.status_code].get(
                            'message')

                    message = f"""{red("[CONSUMER MESSAGE]:", "bold")} Ha ocurrido un error en la URL {url}
            {red("Código:", "bold")} {response.status_code}
             {red("Error:", "bold")} {error_detail}"""

                    print(message)

                    continue

            except Exception:
                print(
                    f'{red("[CONSUMER MESSAGE]:", "bold")} No hay conexión a internet')

            sleep(robot_config['delay'])

except KeyboardInterrupt:
    print(f'{yellow("[CONSUMER MESSAGE]:", "bold")} Ejecución detenida')
