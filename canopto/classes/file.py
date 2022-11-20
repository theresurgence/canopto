import os

from core.config import get_download_dir
from core.web import download_file, url_download_file


class File:

    def __init__(self, m_id: str, file_name: str, size: str, folder_path: str):
        self.id = int(m_id)
        self.path = os.path.join(folder_path, file_name.replace('/', '-'))
        self.size = int(size)

    async def download(self) -> None:
        url = url_download_file(self.id)
        await download_file(url, self.abs_path())

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def abs_path(self) -> str:
        return os.path.join(get_download_dir(), self.path)

    def same_size(self) -> bool:
        return os.path.getsize(self.abs_path()) == self.size

    def create_dir(self) -> None:
        os.makedirs(self.abs_path())
