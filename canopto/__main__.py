#!/bin/python3
import asyncio

from classes.courses import Courses
from core.authenticate import authentication_loop
from core.config import parse_config_file
from core.menu import select_menu
from core.web import close_aclient


# logging.basicConfig(filename='logfile.txt', level=logging.INFO)


async def main():
    await parse_config_file()
    is_authenticated = await authentication_loop()

    if is_authenticated:
        courses = Courses('student')
        await courses.refresh_list()

        await select_menu(courses)

    await close_aclient()


def cli():
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, RuntimeError):
        print("Exited.")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, RuntimeError):
        print("Exited.")
