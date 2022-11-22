import logging
import os
import sys
import time

import httpx

from classes.menuoption import MenuOption
from core.authenticate import logout_credentials_from_keyring
from core.config import select_download_dir_dialog
from ui.messages import print_download_time, print_request_error, print_faq
from ui.tui import select_option_prompt


async def download_files(courses):
    logging.info("Downloading files....")
    start = time.perf_counter()
    await courses.download_files()
    end = time.perf_counter() - start
    time_taken = f'{end:0.2f}'
    print_download_time("files", time_taken)


async def download_videos(courses):
    logging.info("Downloading videos....")
    start = time.perf_counter()
    await courses.refresh_videos_list()
    await courses.download_videos()

    end = time.perf_counter() - start
    time_taken = f'{end:0.2f}'
    print_download_time("videos", time_taken)


async def download_files_and_videos(courses):
    await download_files(courses)
    await download_videos(courses)


def show_faq():
    print_faq()


def clear_screen():
    if sys.platform == "win32":
        os.system('cls')
    else:
        os.system('clear')


async def select_menu(courses):
    clear_screen()

    while True:
        option = await select_option_prompt(courses)

        logging.info(f"Option selected: {option}")
        clear_screen()

        try:
            if option == MenuOption.DL_ALL:
                await courses.refresh_contents()
                await download_files_and_videos(courses)

            elif option == MenuOption.DL_FILES:
                await courses.refresh_contents()
                await download_files(courses)

            elif option == MenuOption.DL_VIDEOS:
                await courses.refresh_contents()
                await download_videos(courses)

            elif option == MenuOption.SEL_FOLDER:
                await select_download_dir_dialog()

            elif option == MenuOption.FAQ:
                show_faq()

            elif option == MenuOption.LOGOUT:
                username = logout_credentials_from_keyring()
                print(f"{username} has been logged out!")
                break

            elif option == MenuOption.QUIT:
                break

        except httpx.RequestError as exc:
            print_request_error()
            logging.error(f"Menu: An error occurred while requesting {exc.request.url!r}.")
            break
