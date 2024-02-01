import smtplib
import ssl
import json
import os
import time
from email.message import EmailMessage
from pathlib import Path
from time import sleep, struct_time
from typing import Dict

import requests
from simple_colors import *

from http_status_codes import RESPONSE_CODES


class RobotConsumer:
    __smtp_server: str = 'smtp.gmail.com'
    __port: int = 587
    __context = ssl.create_default_context()
    __message = EmailMessage()
    __consumer_config: Dict = {}
    __error_flag: bool = False
    __error: str = ''
    __current_time: struct_time = time.localtime(time.time())
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
                if time.strftime('%H:%M', self.__current_time) > self.__consumer_config['startTime'] and time.strftime('%H:%M', self.__current_time) < self.__consumer_config['stopTime']:
                    for url in self.__consumer_config['robotsUrls']:
                        print(
                            f'{green("[CONSUMER MESSAGE]", "bold")} Consultando {url}')

                        try:
                            response = requests.get(url, timeout=60)
                            response.raise_for_status()

                            print(
                                f'{green("[CONSUMER MESSAGE]", "bold")} {time.strftime("%H:%M:%S", self.__current_time)}: Respuesta {response.status_code} {RESPONSE_CODES[response.status_code].get("message")}')

                        except requests.exceptions.HTTPError as e:
                            print(
                                f'{red("[CONSUMER MESSAGE]", "bold")} {time.strftime("%H:%M:%S", self.__current_time)}: Ha ocurrido el siguiente error:\n\n{e}\n')

                            self.__error_flag = True
                            self.__error = str(e)

                            break

                        finally:
                            print(
                                '######################################################')

                        sleep(self.__consumer_config['delay'])
                else:
                    sleep(60.0)

                if self.__error_flag:
                    self.__send_email(self.__error)

                    print(
                        f'\n{red("[CONSUMER MESSAGE]", "bold")} {time.strftime("%H:%M:%S", self.__current_time)}: Ejecución detenida debido a un error\n')
                    print('######################################################')

                    exit(-1)

                self.__current_time = time.localtime(time.time())

        except KeyboardInterrupt:
            print(
                f'{yellow("[CONSUMER MESSAGE]", "bold")} {time.strftime("%H:%M:%S", self.__current_time)}: Ejecución detenida')

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

    def __send_email(self, error) -> None:
        try:
            server = smtplib.SMTP(self.__smtp_server, self.__port)
            server.starttls(context=self.__context)
            server.login(
                self.__consumer_config['sender_email'], self.__consumer_config['password'])

            self.__message['Subject'] = 'Error en el robot'
            self.__message['From'] = self.__consumer_config['sender_email']
            self.__message['To'] = self.__consumer_config['receiver_email']
            self.__message.set_content(
                f'Ha ocurrido el siguiente error:\n{error}')

            server.send_message(self.__message)

            print(
                f'{green("[CONSUMER MESSAGE]", "bold")} {time.strftime("%H:%M:%S", self.__current_time)}: Correo enviado.')

        except Exception as e:
            print(
                f'{red("[CONSUMER MESSAGE]", "bold")} {time.strftime("%H:%M:%S", self.__current_time)}: Ocurrió el siguiente error:\n\n{e}')

        finally:
            server.quit()
