import json
import os
from pathlib import Path
from time import sleep
from typing import Dict

import requests
from http_status_codes import CLIENT_ERRORS_DICT, SERVER_ERRORS_DICT
from simple_colors import *


class RobotConsumer:
    __consumer_config: Dict = {}
    __error_detail: str = ''
    __BAR_LEN = 24
    __BAR_ELEMENTS = ['-', '\\', '|', '/']

    def __init__(self, dirname: str, filename: str):
        """
        Initialize a RobotConsumer instance.

        Args:
            dirname (str): Name of the directory where the file will be searched.
            filename (str): Name of the configuration file.

        Returns:
            None
        """

        self.__dirname = dirname
        self.__filename = filename
        self.__dirpath = self.__get_dirpath()

        self.__set_robot_config()

    def start(self):
        """
        Starts the execution of the robots consumer.

        Returns:
            None
        """

        print(f'\n{yellow("[CONSUMER MESSAGE]", "bold")} Iniciando ejecución')

        try:
            while True:
                for url in self.__consumer_config['robotsUrls']:
                    print(
                        f'{green("[CONSUMER MESSAGE]", "bold")} Consultando {url}')

                    try:
                        response = requests.get(url)

                        if response.status_code in CLIENT_ERRORS_DICT:
                            self.__error_detail = CLIENT_ERRORS_DICT[response.status_code].get(
                                'message')
                        elif response.status_code in SERVER_ERRORS_DICT:
                            self.__error_detail = SERVER_ERRORS_DICT[response.status_code].get(
                                'message')

                        if self.__error_detail != '':
                            message = f"""{red("[CONSUMER MESSAGE]", "bold")} Ha ocurrido un error en la URL {url}
            {red("Código:", "bold")} {response.status_code}
             {red("Error:", "bold")} {self.__error_detail}"""

                            print(message)

                            continue

                    except Exception:
                        print(
                            f'{red("[CONSUMER MESSAGE]", "bold")} No hay conexión a internet')

                    sleep(self.__consumer_config['delay'])

        except KeyboardInterrupt:
            print(f'{yellow("[CONSUMER MESSAGE]", "bold")} Ejecución detenida')

    def __get_dirpath(self) -> str | None:
        """
        Gets the absolute path of the directory where the file will be searched.

        Returns:
            str | None: Absolute path of the directory or None if not find.
        """
        counter = 0
        os.chdir(Path.home())

        if 'Documents' in os.listdir(Path.cwd()):
            os.chdir(Path.cwd() / 'Documents')

        path = Path.cwd()

        for current_path, directories, _ in os.walk(path):
            if counter > self.__BAR_LEN:
                counter = 0

            frame = counter % len(self.__BAR_ELEMENTS)

            print(
                f'\r{yellow("[CONSUMER MESSAGE]", "bold")} Buscando el directorio {yellow(f"{self.__dirname}", ["bold", "italic"])} \
                  [{self.__BAR_ELEMENTS[frame] * counter:=<{self.__BAR_LEN}}]', end='')

            if self.__dirname in directories:
                return os.path.join(current_path, self.__dirname)

            counter += 1

            sleep(0.2)

        return None

    def __set_robot_config(self) -> None:
        """
        Sets initial configuration for the consumer.

        Returns:
            None
        """

        if not self.__file_in_dir():
            raise Exception(
                f'{red("[CONSUMER MESSAGE]", "bold")} El archivo {yellow("robots.json", ["bold", "italic"])} no existe en el directorio actual')

        with open(Path(self.__dirpath) / self.__filename) as f:
            try:
                self.__consumer_config = json.loads(f.read())
            except json.JSONDecodeError as error:
                raise Exception(
                    f'{red("[CONSUMER MESSAGE]", "bold")} El JSON está mal estructurado, por favor revísalo')
            finally:
                f.close()

    def __file_in_dir(self) -> bool:
        """
        Validates if the file exists in the directory.

        Returns:
            bool: True if is in the directory, False otherwise.
        """
        dir_files = os.listdir(self.__dirpath)

        return self.__filename in dir_files
