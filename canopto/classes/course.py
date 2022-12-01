import asyncio
import logging
import os

from bs4 import BeautifulSoup

from canopto.classes.folder import Folder
from canopto.core.config import get_download_dir
from canopto.core.web import ep_folders_in_course, get_json
from canopto.core.web import get_ext_tools_panopto_url, get_request, post_request, create_folder_request_payload

PANOPTO_LTI_URL = 'https://mediaweb.ap.panopto.com/Panopto/LTI/LTI.aspx'
FOLDER_INFO_URL = 'https://mediaweb.ap.panopto.com/Panopto/Services/Data.svc/GetFolderInfo'
FOLDER_SESSION_URL = 'https://mediaweb.ap.panopto.com/Panopto/Services/Data.svc/GetSessions'


class Course:

    def __init__(self, m_id: int, name: str, code: str, role):
        self.id = m_id
        self.name = name.replace('/', '-')
        self.code = code
        self.role = role
        self.folders = []
        self.videos = {}

    def __repr__(self):
        return f'{self.name}  {self.role}'

    async def download_files(self) -> None:
        await self.create_dirs()
        await asyncio.gather(*[folder.download_files() for folder in self.folders if folder.authorized])

    async def refresh_contents(self) -> None:
        folders_json = await get_json(ep_folders_in_course(self.id))

        self.folders = [Folder(f["id"], f["full_name"], self.code)
                        for f in folders_json]

        for i in self.folders:
            logging.info(f'Folder ID {i.id}. Path: {i.path}')

        await asyncio.gather(*[folder.refresh() for folder in self.folders])

    async def create_dirs(self) -> None:
        await asyncio.gather(*[folder.create_dir() for folder in self.folders])

    """
    VIDEO
    """

    @staticmethod
    def get_subfolders(folder_path, json_data):
        if len(json_data['d']['Subfolders']) > 0:
            return {os.path.join(folder_path,
                                 i['Name'].replace('/', '-')):
                        i['ID'] for i in json_data['d']['Subfolders']}
        return {}

    @staticmethod
    def get_video_urls(folder_path, json_data):
        if len(json_data['d']['Results']) > 0:
            return {os.path.join(folder_path,
                                 i['SessionName'].replace('/', '-') + '.mp4'):
                        i['IosVideoUrl'] for i in json_data['d']['Results']}
        return {}

    # Extract folder_id from redirected url
    # folder_id = 'd390e6d6-ded7-4bef-870e-aee000201477'
    @staticmethod
    def get_folderid_from_url(url):
        trunc_url = url[url.find('folderID=') + 9:]
        return trunc_url[:trunc_url.find('&')]

    async def get_videos(self):
        # Access panopto through canvas
        url = get_ext_tools_panopto_url(self.id)
        r = await get_request(url)

        # LTI Post request to get .ASPXAUTH COOKIES to Panopto
        data = {i['name']: i['value']
                for i in BeautifulSoup(r.text, 'html.parser').find_all('input')}
        r = await post_request(PANOPTO_LTI_URL, data=data, follow_redirects=True)

        prev_url = str(r.history[-1].url)
        folder_id = self.get_folderid_from_url(prev_url)
        videos_download_dir = os.path.join(get_download_dir(), self.code, 'Videos_Panopto')

        await self.get_video_dict(videos_download_dir, folder_id)

    async def get_video_dict(self, folder_path, folder_id):

        # Get current panopto course folder data
        json_data = create_folder_request_payload(folder_id)
        r = await post_request(FOLDER_SESSION_URL, data=None, json=json_data)

        # Get video urls and subfolders from current panopto course folder
        self.videos.update(self.get_video_urls(folder_path, r.json()))
        subfolders = self.get_subfolders(folder_path, r.json())

        for folder_path, folder_id in subfolders.items():
            await self.get_video_dict(folder_path, folder_id)
