import logging
import os
import sys
import time

import httpx

from canopto.classes.menuoption import MenuOption
from canopto.core.config import select_download_dir_dialog
from canopto.ui.messages import print_download_time, print_request_error, print_faq
from canopto.ui.tui import select_option_prompt


async def download_files(courses):
    start = time.perf_counter()
    await courses.download_files()
    end = time.perf_counter() - start
    time_taken = f'{end:0.2f}'
    print_download_time("files", time_taken)


async def download_videos(courses):
    start = time.perf_counter()
    for course in courses.courses:
        await course.get_videos()
    await course.download_videos()
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
        clear_screen()

        try:
            if option == MenuOption.DL_ALL:
                await download_files_and_videos(courses)

            elif option == MenuOption.DL_FILES:
                await download_files(courses)

            elif option == MenuOption.DL_VIDEOS:
                await download_videos(courses)

            elif option == MenuOption.SEL_FOLDER:
                await select_download_dir_dialog()

            elif option == MenuOption.FAQ:
                show_faq()

            elif option == MenuOption.QUIT:
                break

        except httpx.RequestError as exc:
            print_request_error()
            logging.error(f"Menu: An error occurred while requesting {exc.request.url!r}.")
            break
