import tkinter as tk
from tkinter import filedialog

import aiofiles
import aiofiles.os

download_dir = ''
CONFIG_FILE_PATH = '.canopto_config.txt'


async def parse_config_file():
    """
    Config file should only have download directory at the moment.
    Might have more variables in future.
    Sets the download_dir based on path given in the config file
    """
    if await aiofiles.os.path.exists(CONFIG_FILE_PATH):
        async with aiofiles.open(CONFIG_FILE_PATH, mode='r') as file:
            path = await file.read()
            if await aiofiles.os.path.isdir(path):
                set_download_dir(path)

    return None


async def write_config_file():
    async with aiofiles.open(CONFIG_FILE_PATH, mode='w') as file:
        await file.write(f'{download_dir}')


async def select_download_dir_dialog():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    if path != tuple() and path != '':
        set_download_dir(path)
        await write_config_file()


def get_download_dir():
    return download_dir


def set_download_dir(path: str):
    global download_dir
    download_dir = path


async def is_download_dir_valid():
    return await aiofiles.os.path.isdir(download_dir)
