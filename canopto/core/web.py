import copy
import pickle
from pathlib import Path

import aiofiles
import aiofiles.os
import httpx

API_BASE_URL = 'https://canvas.nus.edu.sg/api/v1/'
BROWSER_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/clientp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers'
}

LIMITS = httpx.Limits(max_keepalive_connections=None, max_connections=10)
ACLIENT = httpx.AsyncClient(http1=False, http2=True,
                            limits=LIMITS,
                            headers=BROWSER_HEADER, timeout=10)


async def close_aclient():
    await ACLIENT.aclose()


async def get_request(url, follow_redirects=False):
    res = await ACLIENT.get(url, follow_redirects=follow_redirects)
    if res.status_code >= 400 and res.status_code != 403:
        res.raise_for_status()
    return res


async def post_request(url, data=None, json=None, follow_redirects=False):
    res = await ACLIENT.post(url, data=data, json=json,
                             follow_redirects=follow_redirects)
    if res.status_code >= 400:
        res.raise_for_status()
    return res


async def get_json(api_endpoint: str):
    url = API_BASE_URL + api_endpoint + '?per_page=100'
    response = await get_request(url)
    return response.json()


async def stream_download(headers, url, file_path, file_path_part):
    async with aiofiles.open(file_path_part, mode='ab') as file:
        print(f"Downloading {file_path} ...")
        async with ACLIENT.stream('GET', url, headers=headers, follow_redirects=True) as res:
            res.raise_for_status()
            async for chunk in res.aiter_bytes():
                await file.write(chunk)
        print(f"Finished downloading {file_path}!")


async def download_file(url, path):
    """
Partially downloaded files are created with .part extension.
Even if download stops halfway, it can be resumed from where it left off.
Once fully downloaded, .part extension is removed.
Files stored locally without .part are ignored.
    @param url: url of file to be downloaded
    @param path: absolute path of file to be downloaded
    """
    file_path = Path(path)
    file_path_part = Path(f'{path}.part')

    if file_path_part.exists():
        file_part_size = file_path_part.stat().st_size
        headers = copy.deepcopy(BROWSER_HEADER)
        headers.update({'Range': f'bytes={file_part_size}-'})
        await stream_download(headers, url, file_path, file_path_part)
        await aiofiles.os.rename(file_path_part, file_path)

    else:
        if not file_path.exists():
            await stream_download(BROWSER_HEADER, url, file_path, file_path_part)
            await aiofiles.os.rename(file_path_part, file_path)


def url_download_file(file_id) -> str:
    return f'https://canvas.nus.edu.sg/files/{file_id}/download?download_frd=1'


def ep_personal_folders() -> str:
    return "users/self/folders"


def ep_courses() -> str:
    return "courses"


def ep_folders_in_course(course_id: int) -> str:
    return f'courses/{course_id}/folders/'


def ep_files_in_folder(folder_id: int) -> str:
    return f'folders/{folder_id}/files/'


def get_ext_tools_panopto_url(course_id):
    return f'https://canvas.nus.edu.sg/courses/{course_id}/external_tools/128'


# Can use this to arbitrarily search panopto videos
def create_folder_request_payload(folderId):
    return {
        "queryParameters": {
            # "bookmarked": False,
            # "endDate": None,
            "folderID": folderId,
            "getFolderData": True,
            "includeArchived": True,
            "includeArchivedStateCount": True,
            "includePlaylists": True,
            # "isSharedWithMe": False,
            # "isSubscriptionsPage": False,
            # "maxResults": 25,
            # "page": 0,
            # "query": None,
            "sessionListOnlyArchived": False,
            "sortAscending": True,
            # "sortColumn": 1,
            # "startDate": None
        }
    }


def save_cookies(cookies_file):
    with open(cookies_file, "wb") as f:
        pickle.dump(ACLIENT.cookies.jar._cookies, f)


def load_cookies(cookies_file):
    with open(cookies_file, "rb") as f:
        loadedCookies = pickle.load(f)

    ACLIENT.cookies.jar._cookies.update(loadedCookies)
    ACLIENT.cookies.jar.clear_expired_cookies()
