import asyncio
import logging
import os

import aiofiles

from canopto.classes.file import File
from canopto.core.config import get_download_dir
from canopto.core.web import ep_files_in_folder, get_json


class Folder:

    def __init__(self, m_id: int, path: str, course_code: str):
        self.id = m_id
        self.path = path.replace('course files', course_code)  # replace default folder name given by canvas
        self.authorized = True
        self.files = []

    async def download_files(self) -> None:
        await asyncio.gather(*[file.download() for file in self.files])

    def exists(self) -> bool:
        return os.path.exists(self.path)

    async def refresh(self) -> None:
        files_json = await get_json(ep_files_in_folder(self.id))

        try:
            if files_json.get('status') == 'unauthorized':
                self.authorized = False
                logging.info(f'UNAUTHORIZED Folder{self.id}')
        except:  # TODO empty except
            pass

        if self.authorized:
            self.files = [
                File(f["id"], f["display_name"], f["size"], self.path)
                for f in files_json]

    def abs_path(self) -> str:
        return os.path.join(get_download_dir(), self.path)

    async def create_dir(self) -> None:
        logging.info(self.abs_path())
        await aiofiles.os.makedirs(self.abs_path(), exist_ok=True)
