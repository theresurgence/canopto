import logging
import os

from canopto.core.config import get_download_dir
from canopto.core.web import download_file


class File:

    def __init__(self, m_id: str, file_name: str, size: str, url: str, folder_path: str):
        self.id = int(m_id)
        self.path = os.path.join(folder_path, file_name.replace('/', '-'))
        self.size = int(size)
        self.url = url

    # TODO:https://canvas.nus.edu.sg/files/012345/download?download_frd=1
    # save by exact URL or just have a function that calls the download url
    async def download(self) -> None:
        logging.info(self.url)
        await download_file(self.url, self.abs_path())

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def abs_path(self) -> str:
        return os.path.join(get_download_dir(), self.path)

    def same_size(self) -> bool:
        return os.path.getsize(self.abs_path()) == self.size

    def create_dir(self) -> None:
        os.makedirs(self.abs_path())
